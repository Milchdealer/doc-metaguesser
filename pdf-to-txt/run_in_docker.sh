#!/usr/bin/env bash
# Needs a SQL connection specified via the ENV variable TXT_METAGUESSER__SQL_ALCHEMY__URI

if [ -z $TXT_METAGUESSER__SQL_ALCHEMY__URI ]; then
	echo "TXT_METAGUESSER__SQL_ALCHEMY__URI is not set!"
	exit 1
fi

# Variables
TMP_DIR=/tmp/`date +%F"-"%H%M`

# Build the docker images
docker build -t pdf-to-text ./pdf-to-text
docker build -t txt-metaguesser ./txt-metaguesser

# Parse all input directories
for INPUT_DIR in "$@"
do
	TMP_OUT_DIR=$TMP_DIR/$INPUT_DIR
	mkdir -p $TMP_OUT_DIR

	docker run --read-only -v ${INPUT_DIR}:/input -v ${TMP_OUT_DIR}:/output pdf-to-text:latest
	docker run --read-only -v ${TMP_OUT_DIR}:/input \
		-e TXT_METAGUESSER__SQL_ALCHEMY__URI=${TXT_METAGUESSER__SQL_ALCHEMY__URI} \
		txt-metaguesser:latest

	rm -rf $TMP_OUT_DIR
done