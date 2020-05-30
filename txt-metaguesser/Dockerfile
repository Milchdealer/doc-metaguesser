# Docker image for guessing meta information about documents.
FROM python:3.7-slim

LABEL MAINTAINER="Milchdealer"
LABEL DESCRIPTION="Reads text and guesses meta information."

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  DEBIAN_FRONTEND=noninteractive

# Since the datetime setting for month's names needs locales:
# E.g. 1. Januar 2020 in DE will be 1. January 2020 in EN
ARG LOCALE="de_DE.UTF-8"
ARG LANGUAGE="de_DE"
RUN apt-get update && apt-get install -y --no-install-recommends locales \
	&& locale-gen $LOCALE \
	&& dpkg-reconfigure --frontend=noninteractive locales \
	&& localedef -f UTF-8 -i $LANGUAGE $LOCALE \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

ARG INPUT_DIR="/input"
ENV TXT_METAGUESSER__INPUT_DIR=${INPUT_DIR}
RUN pip install pipenv && mkdir /txt-metaguesser && mkdir ${TXT_METAGUESSER__INPUT_DIR}
VOLUME ${TXT_METAGUESSER__INPUT_DIR}

WORKDIR /txt-metaguesser
COPY Pipfile /txt-metaguesser/
RUN pipenv install --deploy --ignore-pipfile

COPY src/ /txt-metaguesser/
ARG PLUGINS="meta_date"
ENV TXT_METAGUESSER__PLUGINS=${PLUGINS}

ENTRYPOINT ["pipenv", "run", "python3"]
CMD ["main.py"]
