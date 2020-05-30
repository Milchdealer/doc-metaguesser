# *-* coding: utf-8 *-*
"""
    Tries to guess metadata about PDF documents.
"""
import logging
import os
import mimetypes

from db import make_connection, create_relations
from doc_utils import get_or_create_document
from meta_utils import guess_metadata

if __name__ == "__main__":
    input_path = os.getenv("TXT_METAGUESSER__INPUT_DIR", "/input")
    engine, session = make_connection()
    create_relations(engine)

    documents = []
    for subdir, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if mimetypes.guess_type(file_path)[0] != "text/txt":
                continue
            logging.debug("Found txt file %s", file_path)
            documents.append(get_or_create_document(file_path, session))

    for document in documents:
        guess_metadata(document, session)

else:
    logging.warning("Imported main.py file which is an entrypoint")
