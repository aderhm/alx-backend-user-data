#!/usr/bin/env python3
"""Module: Regex-ing"""

import logging
import mysql
import os
import re
from mysql.connector import connection
from typing import List

PII_FIELDS = ('password', 'ssn', 'name', 'email', 'phone')


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize obejct.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Hides personal data.
        """
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Returns the log message obfuscated.
    """
    return re.sub(r'({})=([^{}]*)'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator)
        ), lambda m: f"{m.group(1)}={redaction}", message)


def get_logger() -> logging.Logger:
    """Returns a logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database.
    """
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    hostname = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")

    cnx = mysql.connector.connection.MySQLConnection(
        host=hostname,
        database=db,
        username=username,
        password=password)
    return cnx


def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};"
        print(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
