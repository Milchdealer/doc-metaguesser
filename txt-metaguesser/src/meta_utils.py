# *-* coding: utf-8 *-*
"""
	Utilities for guessing metadata.
"""
import re
from datetime import datetime

from db import DocumentStore

DATE_REGEX = re.compile("")


def read_dates(document: DocumentStore, max_lines: int = 100):
    """ Tries to read dates in the content of the document. """

    def _read_date(line: str):
        pass

    for counter, line in enumerate(document.content):
        if counter >= max_lines:
            break

        _read_date(line)


def guess_type(document: DocumentStore):
    """ Guesses the type of the entry. """
    pass


def guess_metadata(document: DocumentStore, session):
    """  Entry point to start guessing metadata."""
    guess_type(document)  # letter, article, ...
    # switch type and go from here
