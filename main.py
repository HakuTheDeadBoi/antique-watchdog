import threading
import schedule
import time
import importlib
import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

## consts
SCRIPT_DIR = 'scripts'

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

def send_mail(records):
    date_time_stamp = get_date_time_stamp()
    smtp_server = config.smtp_server
    smtp_port = config.smtp_port

    email_address = config.user_mail
    password = config.user_pass
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

def run_scripts():
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

    send_mail(records)

def threaded_run(fc):
     fc_thread = threading.Thread(target=fc)
     fc_thread.start()

def main():
    run_scripts()
    schedule.every().day.at("06:00", "Europe/Prague").do(threaded_run, run_scripts)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()