# *-* coding: utf-8 *-*
"""
    Module to for date related metadata.

    To define which patterns to use in which order, specify the TXT_METAGUESSER__META_DATE__PATTERNS
    env variable with a comma-separated list of the dictionary names.
    Example:
    ```sh
    export TXT_METAGUESSER__META_DATE__PATTERNS="GERMAN_LONG,GERMAN_SHORT"
    ```
"""
import os
import re
import locale
import logging
from datetime import datetime
from typing import Optional, List, Dict

from db import DocumentStore, MetadataStore

LOCALE = os.getenv("TXT_METAGUESSER__META_DATE__LOCALE")
PATTERNS = {
    "GERMAN_LONG": {
        "regex": re.compile(r"(\d{2}\.\d{2}\.\d{4})"),
        "date_pattern": "%d.%m.%Y",
    },
    "GERMAN_SHORT": {
        "regex": re.compile(r"(\d{2}\.\d{2}\.\d{2})"),
        "date_pattern": "%d.%m.%y",
    },
    "GERMAN_LOCALE": {
        "regex": re.compile(r"(\d{1,2}\.\s\S+\s\d{4})"),
        "date_pattern": "%d. %B %Y",
    },
}


def search_date_in_line(patterns: List[Dict], line: str) -> Optional[datetime]:
    """ Tries to find the date in the input. """
    for pattern in patterns:
        match = pattern["regex"].search(line)
        if match:
            try:
                date_string = match.group(0)
                if "marz" in date_string.lower():
                    date_string = date_string.replace("a", "ä")
                return datetime.strptime(date_string, pattern["date_pattern"])
            except ValueError:
                pass

    return None


def guess_metadata(document: DocumentStore) -> MetadataStore:
    """ Default callable which is used by guess_metadata() if this plugin is imported.
        :param document: DocumentStore, Document to guess metadata for
        :returns MetadataStore:
    """
    pattern_names = os.getenv(
        "TXT_METAGUESSER__META_DATE__PATTERNS",
        "GERMAN_LONG,GERMAN_SHORT,GERMAN_LOCALE",
    )
    patterns = [PATTERNS[name] for name in pattern_names.split(",") if name in PATTERNS]
    if not patterns:
        raise ValueError("No pattern specified")

    if LOCALE:
        old_locale = ".".join(locale.getlocale())
        logging.info("Changing locale temporarily from %s to %s", old_locale, LOCALE)
        locale.setlocale(locale.LC_ALL, LOCALE)

    for line in document.content.split("\n"):
        document_date = search_date_in_line(patterns, line)
        if document_date:
            return MetadataStore(
                document_id=document.id,
                metadata_label="document_date",
                metadata_value=document_date.strftime("%Y-%m-%d"),
            )

    if LOCALE and old_locale:
        locale.setlocale(locale.LC_ALL, old_locale)
        logging.debug("Changed locale back to %s", old_locale)
