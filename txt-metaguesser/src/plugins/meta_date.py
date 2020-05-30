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
from datetime import datetime
from typing import Optional, List, Dict

from db import DocumentStore, MetadataStore

PATTERNS = [
    {
        "GERMAN_LONG": {
            "regex": re.compile(r"\d{2}\.\d{2}\.\d{4}"),
            "date_pattern": "%d.%m.%Y",
        }
    },
    {
        "GERMAN_SHORT": {
            "regex": re.compile(r"\d{2}\.\d{2}\.\d{2}"),
            "date_pattern": "%d.%m.%y",
        }
    },
]


def _validate_patterns(patterns: List[Dict]) -> bool:
    """ Validates the patterns passed for their data structure. """

    def _validate_pattern(pattern: Dict) -> bool:
        return "regex" in pattern and "date_pattern" in pattern

    all([_validate_pattern(p) for p in patterns])


def search_date_in_line(patterns: List[Dict], line: str) -> Optional[datetime]:
    """ Tries to find the date in the input. """
    for pattern in patterns:
        last_match = pattern["regex"].search(line)
        if last_match:
            return datetime.strptime(last_match.group(0), pattern["date_pattern"])
    return None


def guess_metadata(document: DocumentStore) -> MetadataStore:
    """ Default callable which is used by guess_metadata() if this plugin is imported.
        :param document: DocumentStore, Document to guess metadata for
        :returns MetadataStore:
    """
    pattern_names = os.getenv(
        "TXT_METAGUESSER__META_DATE__PATTERNS", "GERMAN_LONG,GERMAN_SHORT"
    )
    patterns = [PATTERNS[name] for name in pattern_names.split(",") if name in PATTERNS]
    if not patterns:
        raise ValueError("No pattern specified")
    if not _validate_patterns(patterns):
        raise ValueError("Received an invalid data structure for patterns")

    for line in document.content:
        document_date = search_date_in_line(patterns, line)
        if document_date:
            return MetadataStore(
                document_id=document.id,
                metadata_label="document_date",
                metadata_value=document_date.strftime("%Y-%m-%d"),
            )
