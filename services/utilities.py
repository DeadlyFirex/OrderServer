from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from random import choice
from functools import wraps
from uuid import UUID

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
        Generates a token timedelta
        Returns a timedelta

        TODO: Make this configurable
        :return: Timedelta
        """
        result = timedelta(days=1)
        return result

    @staticmethod
    def return_response(status=200, message="This is a message"):
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
    def return_complex_response(status=200, message="This is a message", details=None):
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
    def return_custom_response(status=200, message="This is a message", extra=None):
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
        result.update(extra)
        return result, status

    @staticmethod
    def return_result(status=200, message="This is a message", result=None):
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
        time = round((end - start).total_seconds() * 1000, 2)
        return f"{time}ms"

    @staticmethod
    def is_valid_uuid(value):
        try:
            UUID(value)
            return True
        except ValueError:
            return False


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            from models.user import User
            user = User.query.filter_by(uuid=get_jwt_identity()).first()
            if user.admin:
                return fn(*args, **kwargs)
            else:
                return Utilities.return_response(403, "Forbidden, no rights to access admin resources")
        return decorator
    return wrapper


