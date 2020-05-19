# *-* coding: utf-8 *-*
"""
	Module to for date related metadata.
"""
import re
from datetime import datetime, date
from typing import Generator


class DateMatching:
	""" Class for matching dates in strings. """
   	GERMAN_LONG = {
	    "regex": re.compile(r"\d{2}\.\d{2}\.\d{4}"),
	    "date_pattern": "%d.%m.%Y"
	}
	GERMAN_SHORT = {
		"regex": re.compile(r"\d{2}\.\d{2}\.\d{2}"),
		"date_pattern": "%d.%m.%y"
	}


	def __init__(self, *args):
		self.patterns = *args

    def search_dates_in_line(self, line: str) -> Generator[date, None, None]:
        """ Tries to find the date in the input. """


        last_match = self.REGEX.search(line)
        while last_match:
            yield datetime.strptime(last_match.group(0), self.DATETIME_PAT).date()
            last_match = self.REGEX.search(line, last_match.span()[0] + 1)

