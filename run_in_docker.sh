#!/usr/bin/env bash
# Needs a SQL connection specified via the ENV variable TXT_METAGUESSER__SQL_ALCHEMY__URI

if [ -z $TXT_METAGUESSER__SQL_ALCHEMY__URI ]; then
	echo "TXT_METAGUESSER__SQL_ALCHEMY__URI is not set!"
	exit 1
fi

# Variables
TMP_DIR=/tmp/`date +%F"-"%H%M`

# Build the docker images
docker build -t pdf2txt ./pdf-to-txt

docker build -t txt-metaguesser ./txt-metaguesser

# Parse all input directories
for INPUT_DIR in "$@"
do
	TMP_OUT_DIR=$TMP_DIR/$INPUT_DIR
	mkdir -p $TMP_OUT_DIR

	docker run -v ${INPUT_DIR}:/input:ro -v ${TMP_OUT_DIR}:/output pdf2txt

	docker run -v ${TMP_OUT_DIR}:/input:ro \
		-e TXT_METAGUESSER__SQL_ALCHEMY__URI=${TXT_METAGUESSER__SQL_ALCHEMY__URI} \
		txt-metaguesser

	rm -rf $TMP_OUT_DIR
done

rm -r $TMP_DIR
