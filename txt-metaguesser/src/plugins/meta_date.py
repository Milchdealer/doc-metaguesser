# *-* coding: utf-8 *-*
"""
	Module to for date related metadata.
"""
import re
from datetime import datetime, date
from typing import Generator, List, Dict, Union


class DateMatching:
	""" Class for matching dates in strings. """
   	GERMAN_LONG = {
	    "regex": re.compile(r"\d{2}\.\d{2}\.\d{4}"),
	    "date_pattern": "%d.%m.%Y",
	}
	GERMAN_SHORT = {
		"regex": re.compile(r"\d{2}\.\d{2}\.\d{2}"),
		"date_pattern": "%d.%m.%y",
	}

	@staticmethod
	def _validate_patterns(patterns: List[Dict]) -> bool:
		""" Validates the patterns passed for their data structure. """
		def _validate_pattern(pattern: Dict) -> bool:
			return "regex" in pattern and "date_pattern" in pattern

		all([_validate_pattern(p) for p in patterns])
		
	def __init__(self, patterns: List[str], *args):
		""" List of names of patterns to load, from the class, to load additional ones
			provide the dicts with in form of {"regex": re, "date_pattern": str} as *args.
			They will be loaded in order, and *args before patterns.
		"""
		self.patterns = args + [self.__getattribute__(pattern) for pattern in patterns]

		if not DataMatching._validate_patterns(self.patterns):
			raise ValueError("Received an invalid data structure for patterns")

    def search_dates_in_line(self, line: str) -> Generator[date, None, None]:
        """ Tries to find the date in the input. """
        for pattern in self.patterns:
        	correct_pattern = False
	        last_match = pattern["regex"].search(line)
	        while last_match:
	        	correct_pattern = True
	            yield datetime.strptime(last_match.group(0), pattern["date_pattern"]).date()
	            last_match = pattern["regex"].search(line, last_match.span()[0] + 1)
	        if correct_pattern:
	        	# The patterns usually don't change within a document
	        	break

