# Docker image for OCR with Python
FROM python:3.7

LABEL MAINTAINER="Milchdealer"
LABEL DESCRIPTION="Converts PDFs to images and runs OCR on them \
to convert them to text."

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true

# Install poppler-utils for pdf2image and tesseract-ocr for OCR
RUN apt-get update && apt-get install --yes poppler-utils tesseract-ocr \
	&& apt-get autoremove --yes \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install pipenv


# Create application and input/output directories
RUN mkdir /pdf2txt && mkdir /input && mkdir /output
VOLUME /input
VOLUME /output

WORKDIR /pdf2txt
COPY src/ /pdf2txt/
COPY Pipfile /pdf2txt/
RUN pipenv install --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "python3"]
CMD "main.py --input /input --output /output"
