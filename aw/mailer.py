from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from aw.util import config_loader
from aw.error import CloseThreadError

class Mailer:
    @classmethod
    def _load_config(cls) -> dict[str]:
        keys = [
            "SERVER_ADDR",
            "SERVER_PORT",
            "LOGIN_MAIL",
            "LOGIN_PASSWORD",
            "TARGET_MAIL"
        ]

        config_dict = config_loader(keys)

        return config_dict

    @classmethod
    def _compose_html_records_table(cls, records: list["Record"]) -> str: # type: ignore
        table_header = """\
            <th>Book</th>
            <th>Author</th>
            <th>Price</th>
            <th>Year</th>
            <th>Publisher</th>
            <th>Language</th>
            <th>Link</th>
        """

        html_table = f"<table border='1'><tr>{table_header}</tr>"
        html_table_closing = "</table>"

        for rec in records:
            html_table += f"""
                <tr>
                    <td>{rec.name}</td>
                    <td>{rec.author}</td>
                    <td>{rec.price}</td>
                    <td>{rec.issue_year}</td>
                    <td>{rec.publisher}</td>
                    <td>{rec.language}</td>
                    <td><a href='{rec.link}'>LINK</a></td>
                </tr>
            """

        html_table += html_table_closing

        return html_table
    
    @classmethod
    def _compose_html_document(cls, html_table: str) -> str:
        html_document = f"""
            <html>
                <head>
                    <meta charset='utf-8'>
                    <title>Daily report</title>
                </head>
                <body>
                    {html_table}
                </body>
            <html>
        """

        return html_document
    
    @classmethod
    def _create_mail(cls, html_document: str, sender: str, recipient: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "Daily report"
        message.attach(MIMEText(html_document, "html"))

        return message
    
    @classmethod
    def send_mail(cls, records: list["Record"]) -> int: # type: ignore
        cf = cls._load_config()

        html_table = cls._compose_html_records_table(records)
        html_document = cls._compose_html_document(html_table)
        message = cls._create_mail(html_document, cf["LOGIN_MAIL"], cf["TARGET_MAIL"])

        with smtplib.SMTP_SSL(cf["SERVER_ADDR"], cf["SERVER_PORT"]) as server:
            server.login(cf["LOGIN_MAIL"], cf["LOGIN_PASSWORD"])
            result = server.send_message(message)

            if result != {}:
                raise CloseThreadError("Email sending was not successful.")