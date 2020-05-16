#!/usr/bin/python3
# *-* coding: utf-8 *-*
"""
    Utilities for handling the documents.
"""
from db import DocumentStore, MetadataStore

from typing import TextIO, Optional

MAX_CHECKSUM_INGEST_LENGTH = (
    1000  # If this is changed the checksums won't add up anymore.
)
MAX_CONTENT_LENGTH = 4294967295  # Max size of LONGTEXT in MariaDB
PAGE_SEPARATER = "=" * 50


def create_checksum(document: TextIO, reset_buffer: int = 0) -> str:
    """ Generate the checksum for a file. """
    content = document.read(MAX_CHECKSUM_INGEST_LENGTH)

    if reset_buffer >= 0:
        document.seek(reset_buffer)

    return sha1(content.encode("utf-8")).hexdigest()


def guess_page_num(document: TextIO, reset_buffer: int = 0) -> int:
    """ Tries to guess the page count by counting the PAGE_SEAPARTER. """
    counter = 0
    for line in document:
        if line == PAGE_SEPARATER:
            counter += 1

    if reset_buffer >= 0:
        document.seek(reset_buffer)

    return counter


def create_new_document(
    file_path: str, document: TextIO, reset_buffer: int = 0
) -> DocumentStore:
    """ Creates a new DocumentStore entry. """
    filename = os.path.basename(file_path)
    name = os.path.splitext(filename)[0]
    content = document.read(MAX_CONTENT_LENGTH)
    page_num = guess_page_num(document)
    checksum = create_checksum(document)

    if reset_buffer >= 0:
        document.seek(reset_buffer)

    return DocumentStore(
        name=name,
        filename=filename,
        content=content,
        page_num=page_num,
        checksum=checksum,
    )


def get_or_create_document(file_path: str, session) -> int:
    """ Checks if the file already exists in the store and creates it if not.
        :return int: The id column of the entry
    """
    with open(file_path, "r") as f:
        checksum = create_checksum(f)
        _id = (
            session.query(DocumentStore.id)
            .filter_by(
                DocumentStore.checksum == checksum,
                DocumentStore.filename == os.path.basename(file_path),
            )
            .scalar()
        )
        if not _id:
            ds = create_new_document(file_path, f)
            session.add(ds)
            session.commit()
            _id = ds.id

    return _id
