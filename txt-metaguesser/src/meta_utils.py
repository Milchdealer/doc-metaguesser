# *-* coding: utf-8 *-*
"""
	Utilities for guessing metadata.
"""


def guess_metadata(document_id: int, session):
    """  Entry point to start guessing metadata."""

    content = (
        session.query(DocumentStore.content)
        .filter_by(DocumentStore.id == document_id)
        .first()
    )

    guess_type()  # letter, article, ...
    # switch type and go from here
