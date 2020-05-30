# *-* coding: utf-8 *-*
"""
    Utilities for guessing metadata.
"""
import os
from importlib import import_module
from datetime import datetime

from db import DocumentStore, MetadataStore


def guess_metadata(document: DocumentStore, session):
    """  Entry point to start guessing metadata."""
    plugins = os.getenv("TXT_METAGUESSER__PLUGINS", "meta_date")

    for plugin in plugins.split(","):
        meta_module = import_module(".%s", "plugins")
        metadata = meta_module.guess_metadata()
        existing_metadata = (
            session.query(MetadataStore)
            .filter_by(
                MetadataStore.document_id == document.id,
                MetadataStore.metadata_label == metadata.me,
            )
            .first()
        )

        if existing_metadata:
            existing_metadata.metadata_value = metadata.metadata_value
            existing_metadata.updated_on = datetime.now
        else:
            session.add(metadata)

    session.commit()
