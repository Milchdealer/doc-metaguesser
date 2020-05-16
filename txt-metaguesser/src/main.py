#!/usr/bin/python3
# *-* coding: utf-8 *-*
"""
    Tries to guess metadata about PDF documents.
"""
import logging
import os
import mimetypes
from hashlib import sha1
from typing import TextIO

from db import make_connection, create_relations, DocumentStore, MetadataStore
from doc_utils import get_or_create_document


if __name__ == "__main__":
    input_path = os.getenv("TXT_METAGUESSER__INPUT_DIR", "/input")
    engine, session = make_connection()
    create_relations(engine)

    document_ids = []
    for subdir, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if mimetypes.guess_type(file_path)[0] != "text/txt":
                continue
            logging.debug("Found txt file %s", file_path)
            document_ids.append(get_or_create_document(file_path, session))

    for document_id in document_ids:
        guess_metadata(document_id, session)

else:
    logging.warning("Imported main.py file which is an entrypoint")
