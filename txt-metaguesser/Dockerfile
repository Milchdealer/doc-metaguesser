# Docker image for guessing meta information about documents.
FROM python:3.7

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
  PIPENV_NOSPIN=true

RUN pip install pipenv && mkdir /txt-metaguesser && mkdir /input 
VOLUME /input

ARG SQL_ALCHEMY__URI
ENV SQL_ALCHEMY__URI=${SQL_ALCHEMY__URI}

WORKDIR /txt-metaguesser
COPY src/ /txt-metaguesser/
COPY Pipfile /txt-metaguesser/
RUN pipenv install --deploy --ignore-pipfile

CMD "pipenv run python3 main.py"
