#!/usr/bin/python3
# *-* coding: utf-8 *-*
"""
	Tries to guess metadata about PDF documents.
"""
import logging
import argparse
import os

parser = argparse.ArgumentParser(description="")
parser.add_argument("--input", type=str, required=True, help="Path pointing to a PDF or a folder with PDFs to parse")
parser.add_argument(
	"--silent",
	action="store_const",
	const=True,
	default=False,
	help="Silence all logging, only show output filenames as result"
)
if __name__ == "__main__":
	maria_db_credentials = {
		user: os.getenv("MARIA_DB__USER", "document"),
		host: os.getenv("MARIA_DB__HOST", "localhost"),
		port: int(os.getenv("MARIA_DB__PORT", "3306")),
		database: os.getenv("MARIA_DB__DATABASE", "document"),
		password: os.getenv("MARIA_DB__PASSWORD"),
	}
	db_conn = mariadb.connect(**maria_db_credentials)
	del maria_db_credentials
else:
	parser.parse_args([])