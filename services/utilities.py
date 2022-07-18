from typing import Union

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from flask import request

from random import choice
from functools import wraps
from uuid import UUID
from re import match

from services.config import Config
from datetime import timedelta, datetime

config = Config().get_config()


class Utilities:

    @staticmethod
    def generate_secret():
        """
        Creates a secret-key based on the character-set passed by the configuration.
        Returns a string.

        :return: String, secret-key
        """
        result = ""
        for i in range(0, config.security.secret_length):
            result += choice(config.security.character_list)
        return result

    @staticmethod
    def generate_salt():
        """
        Generates a salt. Painful. Salty.
        Returns a bytes-like.

        :return: Bytes, salt
        """
        result = b""
        for i in range(0, config.security.secret_length):
            result += choice(config.security.character_list).encode("UTF-8")
        return result

    @staticmethod
    def generate_token_timedelta():
        """
        Generates a token timedelta.\n

        :return: Timedelta
        """
        # TODO: Make this configurable
        return timedelta(days=1)

    @staticmethod
    def response(status: int = 200, message: str = "This is a message"):
        """
        Generates an JSON response.
        Returns a dictionary.

        :return: Dictionary
        """
        result = {
            "status": status,
            "message": message
        }
        return result, status

    @staticmethod
    def error_response(status: int = 200, message: str = "This is a message", error: Union[str, dict] = None):
        """
        Generates an JSON response.
        Returns a dictionary.

        :return: Dictionary
        """
        result = {
            "status": status,
            "message": message
        }
        result.update({"error": error})
        return result, status

    @staticmethod
    def detailed_response(status: int = 200, message: str = "This is a message", details: Union[str, dict] = None):
        """
        Generates an JSON response.
        Returns a dictionary.

        :return: Dictionary
        """
        result = {
            "status": status,
            "message": message,
        }
        result.update({"details": details})
        return result, status

    @staticmethod
    def custom_response(status: int = 200, message: str = "This is a message", custom: Union[str, dict] = None):
        """
        Generates a custom JSON response.\n
        Returns a dictionary.\n
        Appends a new dictionary to the standard one.\n

        :return: Dictionary
        """
        result = {
            "status": status,
            "message": message,
        }
        result.update(custom)
        return result, status

    @staticmethod
    def return_result(status: int = 200, message: str = "This is a message", result: Union[str, dict, list] = None):
        """
        Generates an JSON response based on the successful result template.
        Returns a dictionary.

        :return: Dictionary
        """
        result = {
            "status": status,
            "message": message,
            "result": result
        }
        return result, status

    @staticmethod
    def calculate_time(start: datetime, end: datetime = datetime.now()):
        """
        Calculates time difference in milliseconds.\n
        Returns the result in two decimal rounded string.

        :param start: Start datetime object
        :param end: End datetime object
        :return: Time difference in milliseconds, string.
        """
        return f"{round((end - start).total_seconds() * 1000, 2)}ms"

    @staticmethod
    def validate_uuid(value: str):
        """
        Validates if UUIDs are correct.

        :param value: String
        :return: Boolean
        """
        try:
            UUID(value)
        except ValueError:
            return False
        return True

    @staticmethod
    def validate_email(email: str):
        """
        Validates if a string is in email format.

        :param email: String
        :return: Value or None
        """
        if match("""^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$""", email):
            return email
        return None

    @staticmethod
    def validate_phone(phone: str):
        """
        Validates if a string is in phone number format.

        :param phone: String
        :return: Value or None
        """
        if phone.__len__() == 10 and phone.isnumeric():
            return phone
        return None

    @staticmethod
    def validate_postalcode(postal_code: str):
        """
        Validates if a string is in postal format.

        :param postal_code: String
        :return: Value or None
        """
        if match("""^[0-9]{4}[A-Z]{2}$""", postal_code):
            return postal_code
        return None


def admin_required():
    """
    Wrapper that performs user tracking and JWT verification\n
    Only accessible by admins.

    :return: Sir, this is a decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            from models.user import User
            user = User.query.filter_by(uuid=get_jwt_identity()).first()
            if user.admin:
                user.perform_tracking(source=fn.__name__, address=request.remote_addr)
                return fn(*args, **kwargs)
            else:
                return Utilities.response(403, "Forbidden, no rights to access resource")
        return decorator
    return wrapper


def user_required():
    """
    Wrapper that performs user tracking and JWT verification\n
    Accessible by users and admins.

    :return: Sir, this is a decorator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            from models.user import User
            user = User.query.filter_by(uuid=get_jwt_identity()).first()
            if user:
                user.perform_tracking(source=fn.__name__, address=request.remote_addr)
                return fn(*args, **kwargs)
            else:
                return Utilities.response(403, "Forbidden, no rights to access resource")
        return decorator
    return wrapper
