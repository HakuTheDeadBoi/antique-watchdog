import argparse
import datetime
import importlib
import os
import schedule
import smtplib
import threading
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## consts
SCRIPT_DIR = 'scripts'

day_functions = {
    "mon": schedule.every().monday,
    "tue": schedule.every().tuesday,
    "wed": schedule.every().wednesday,
    "thu": schedule.every().thursday,
    "fri": schedule.every().friday,
    "sat": schedule.every().saturday,
    "sun": schedule.every().sunday
}

class Record:
    def __init__(self):
        self.book = ""
        self.author = ""
        self.year = ""
        self.link = ""
        self.publisher = ""
        self.price = ""

    def __str__(self):
        return f"{self.author} - {self.book}: {self.price}"
    
    def __str__(self):
        return f"{self.author} - {self.book}: {self.price}!"
    
def get_date_time_stamp():
    now = datetime.datetime.now()
    return f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
   
def get_script_names():
    script_names = []

    # get file names here
    for filename in os.listdir(SCRIPT_DIR):
        if filename.endswith('.py'):
            script_name = filename[:-3]
            # validate file somehow
            with open(f"{SCRIPT_DIR}/{filename}") as FILE:
                first_line = FILE.readline()
                if first_line.endswith("##\n") and first_line.startswith("##"):
                    script_names.append(script_name)

    return script_names

def send_mail(records, args):
    date_time_stamp = get_date_time_stamp()
    smtp_server = args.server
    smtp_port = args.port

    email_address = args.mail
    password = args.password
    subject = f"Report: {date_time_stamp}"
    body = compose_mail_body(records, date_time_stamp)

    message = MIMEMultipart()
    message["From"] = email_address
    message["To"] = email_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(email_address, password)
        server.send_message(message)
        print(f"Message successfully sent at {date_time_stamp}")

def compose_mail_body(records, date_time_stamp):
    header = f"<h1>Record {date_time_stamp}.</h1>"
    table = compose_html_table(records)
    html = f"<html><body>{header}{table}</body></html>"

    return html

def compose_html_table(records):
    table_header = "<th>Book</th><th>Author</th><th>Price</th><th>Year</th><th>Publisher</th><th>Link</th>"
    html_table = f"<table border='1'><tr>{table_header}</tr>"
    for rec in records:
        html_table += f"<tr><td>{rec.book}</td><td>{rec.author}</td><td>{rec.price}</td><td>{rec.year}</td><td>{rec.publisher}</td><td><a href=\"{rec.link}\">LINK</a></td></tr>"
    html_table += "</table>"

    return html_table

def run_scripts(args):
    records = []

    scripts = get_script_names()

    for script in scripts:
        try:
            module = importlib.import_module(f"{SCRIPT_DIR}.{script}")
        except ImportError as e:
            print(f"Error during importing {script}: {e}")      # later remove and use some log system
        else:
            if hasattr(module, "main"):
                result = module.main(Record)
                if result:
                    for record in result:
                        records.append(record)

    send_mail(records, args)

def threaded_run(fc):
     fc_thread = threading.Thread(target=fc)
     fc_thread.start()

def main():
    # argument parser
    parser = argparse.ArgumentParser(description="Basic scheduler for book antique stores scrapers.")
    parser.add_argument("--mail", required=True, help="Target email.")
    parser.add_argument("--password", required=True, help="Mail password.")
    parser.add_argument("--server", required=True, help="Mail SMTP server.")
    parser.add_argument("--port", required=True, help="SMTP server port.")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--daily", nargs=1, help="Run daily, followed by time in format hh:mm.")
    group.add_argument("--hourly", nargs=1, help="Run hourly, followed by time to start first call in format hh:mm.")
    group.add_argument("--weekly", nargs=2, help="Run weekly, followed by day and time in format mon|tue|wed|thu|fri|sat|sun hh:dd")

    args = parser.parse_args()

    if args.daily:
        schedule.every().day.at(args.daily[0]).do(threaded_run, lambda: run_scripts(args))
    elif args.hourly:
        schedule.every().hour.at(args.hourly[0]).do(threaded_run, lambda: run_scripts(args))
    else:
        day_functions[args.weekly[0]].at(args.weekly[1]).do(threaded_run, lambda: run_scripts(args))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()