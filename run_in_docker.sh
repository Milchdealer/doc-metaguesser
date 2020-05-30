#!/usr/bin/env bash
# Needs a SQL connection specified via the ENV variable TXT_METAGUESSER__SQL_ALCHEMY__URI

if [ -z $TXT_METAGUESSER__SQL_ALCHEMY__URI ]; then
	echo "TXT_METAGUESSER__SQL_ALCHEMY__URI is not set!"
	exit 1
fi

# Variables
TMP_DIR=/tmp/`date +%F"-"%H%M`
echo "Using temporary directory at $TMP_DIR"

# Build the docker images
echo "Building docker image pdf2txt with context ./pdf-to-txt"
docker build -t pdf2txt ./pdf-to-txt
echo "Building docker image txt-metaguesser with context ./txt-metaguesser"
docker build -t txt-metaguesser ./txt-metaguesser

# Parse all input directories
for INPUT_DIR in "$@"
do
	TMP_OUT_DIR=$TMP_DIR/$INPUT_DIR
	mkdir -p $TMP_OUT_DIR
	echo "Created temporary directory $TMP_OUT_DIR"

	echo "Running pdf2txt in docker with ${INPUT_DIR} as input directory"
	docker run -v ${INPUT_DIR}:/input:ro -v ${TMP_OUT_DIR}:/output pdf2txt main.py --input /input --output /output
	echo "Running txt-metaguesser in docker on the result of ${INPUT_DIR}"
	docker run -v ${TMP_OUT_DIR}:/input:ro \
		-e TXT_METAGUESSER__SQL_ALCHEMY__URI=${TXT_METAGUESSER__SQL_ALCHEMY__URI} \
		-e TXT_METAGUESSER__META_DATE__LOCALE="de_DE.UTF-8" \
		txt-metaguesser

	rm -rf $TMP_OUT_DIR
	echo "Removed temporary directory $TMP_OUT_DIR"
done

# Cleanup
rm -r $TMP_DIR
echo "Removed temporary directory $TMP_DIR"
