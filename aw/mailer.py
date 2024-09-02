from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from aw import LOGIN, PASSWORD, RECIPIENT, SERVER, PORT
from aw.config import Config
from aw.error import CloseThreadError


class Mailer:
    @classmethod
    def _compose_html_records_table(cls, records: list["Record"]) -> str: # type: ignore
        """
        Composes an HTML table from a list of records.

        Args:
            records (list[Record]): A list of Record objects to be included in the table.

        Returns:
            str: An HTML string representing the table with the records.
        """
        table_header = """\
            <th>Book</th>
            <th>Author</th>
            <th>Price</th>
            <th>Year</th>
            <th>Publisher</th>
            <th>Language</th>
            <th>Link</th>
        """

        html_table = f"<table border='1' padding='2'><tr>{table_header}</tr>"
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
        """
        Composes an HTML document from the given HTML table.

        Args:
            html_table (str): An HTML string representing the table.

        Returns:
            str: A complete HTML document as a string.
        """
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
        """
        Creates an email message with the given HTML document.

        Args:
            html_document (str): The HTML content of the email.
            sender (str): The sender's email address.
            recipient (str): The recipient's email address.

        Returns:
            MIMEMultipart: The email message object.
        """
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = "Daily report"
        message.attach(MIMEText(html_document, "html"))

        return message
    
    @classmethod
    def send_mail(cls, records: list["Record"], config: Config) -> dict: # type: ignore
        """
        Creates an email message with the given HTML document.

        Args:
            html_document (str): The HTML content of the email.
            sender (str): The sender's email address.
            recipient (str): The recipient's email address.

        Returns:
            MIMEMultipart: The email message object.
        """
        try:
            cf_dict = config.get_mailer_keys()
            login = cf_dict[LOGIN]
            password = cf_dict[PASSWORD]
            recipient = cf_dict[RECIPIENT]
            server = cf_dict[SERVER]
            port = cf_dict[PORT]
        except KeyError as e:
            raise CloseThreadError from e

        html_table = cls._compose_html_records_table(records)
        html_document = cls._compose_html_document(html_table)
        message = cls._create_mail(html_document, login, recipient)

        result = {}

        try:
            with smtplib.SMTP_SSL(server, port) as server:
                server.login(login, password)
                result = server.send_message(message)
        except smtplib.SMTPAuthenticationError as e:
            raise CloseThreadError(f"Autenthication to mail server failed: {e}")
        except smtplib.SMTPConnectError as e:
            raise CloseThreadError(f"Connection to SMTO server failed: {e}")
        except smtplib.SMTPException as e:
            raise CloseThreadError(f"Unexpected error during SMTP connection: {e}")
        
        return result