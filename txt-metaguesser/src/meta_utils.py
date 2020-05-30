# *-* coding: utf-8 *-*
"""
    Utilities for guessing metadata.
"""
import os
import logging
from importlib import import_module

from sqlalchemy import and_

from db import DocumentStore, MetadataStore


def guess_metadata(document: DocumentStore, session):
    """  Entry point to start guessing metadata."""
    plugins = os.getenv("TXT_METAGUESSER__PLUGINS", "meta_date")

    for plugin in plugins.split(","):
        logging.info("Loading plugin %s", plugin)
        meta_module = import_module(".%s" % plugin, "plugins")
        metadata = meta_module.guess_metadata(document)
        if not metadata:
            logging.debug("No metadata found for plugin %s", plugin)
            continue

        existing_metadata = (
            session.query(MetadataStore)
            .filter(
                and_(
                    MetadataStore.document_id == document.id,
                    MetadataStore.metadata_label == metadata.metadata_label,
                )
            )
            .first()
        )

        if existing_metadata:
            existing_metadata.metadata_value = metadata.metadata_value
        else:
            session.add(metadata)

    session.commit()
