import re

from email_validator import validate_email,  EmailNotValidError

class Validator:
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """
        Validates an email address using the `email_validator` library.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            return False
    
    @classmethod
    def validate_port(cls, port: str) -> bool:
        """
        Validates if a given string can be converted to a valid port number.

        Args:
            port (str): The port number to validate.

        Returns:
            bool: True if the port is a valid integer, False otherwise.
        """
        try:
            int(port)
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_server(cls, address: str) -> bool:
        """
        Validates a server address using a regular expression pattern.

        Args:
            address (str): The server address to validate.

        Returns:
            bool: True if the address matches the pattern, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, address) is not None

    @classmethod    
    def validate_time(cls, time: str) -> bool:
        """
        Validates a time string in the format HH:MM (24-hour clock).

        Args:
            time (str): The time string to validate.

        Returns:
            bool: True if the time is valid, False otherwise.
        """
        pattern = r'^(?:[01][0-9]|[2][0-3]):[0-5]{1}[0-9]{1}$'
        return re.match(pattern, time) is not None

