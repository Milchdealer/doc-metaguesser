# *-* coding: utf-8 *-*
"""
	Utilities for guessing metadata.
"""

from db import DocumentStore


def guess_type(document: DocumentStore):
    """ Guesses the type of the entry. """
    pass


def guess_metadata(document: DocumentStore, session):
    """  Entry point to start guessing metadata."""
    guess_type(document)  # letter, article, ...
    # switch type and go from here
