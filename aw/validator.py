import re

from email_validator import validate_email,  EmailNotValidError

class Validator:
    @classmethod
    def validate_email(cls, email: str) -> bool:
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            return False
    
    @classmethod
    def validate_port(cls, port: str) -> bool:
        try:
            int(port)
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_server(cls, address: str) -> bool:
        pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, address) is not None

    @classmethod    
    def validate_time(cls, time: str) -> bool:
        pattern = r'^(?:[01][0-9]|[2][0-3]):[0-5]{1}[0-9]{1}$'
        return re.match(pattern, time) is not None

if __name__ == '__main__':
    print(Validator.validate_email("hdhd@mail.com"))
    print(Validator.validate_email("hdhd@mail.ccm"))
    print(Validator.validate_email("hdhd@com"))

    print(Validator.validate_time("05:05"))
    print(Validator.validate_time("eddeeef"))

    print(Validator.validate_port("555"))
    print(Validator.validate_port("fff"))

    print(Validator.validate_server("hhaha.com"))
    print(Validator.validate_server("dewewfwef"))

