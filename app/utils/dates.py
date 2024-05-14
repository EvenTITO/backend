from datetime import datetime


class DatesException(Exception):
    ERROR_MESSAGE = 'Invalid dates'

    def __init__(self):
        self.error_message = self.ERROR_MESSAGE
        super().__init__(self.error_message)


def validate_date(date):
    if datetime.now() > date:
        raise DatesException()
    else:
        return date
