#!/usr/bin/python3
# *-* coding: utf-8 *-*
"""
	Tries to guess metadata about PDF documents.
"""
import logging
import os

from db import (
	make_connection,
	create_relations,
	DocumentStore,
	MetadataStore
)

if __name__ == '__main__':
	engine, session = make_connection()
	create_relations(engine)

	d1 = DocumentStore(filename="test", content="abc")
	session.add(d1)
	session.commit()
else:
	logging.debug("Imported main.py file which is an entrypoint")
