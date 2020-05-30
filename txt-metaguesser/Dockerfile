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

ENV TXT_METAGUESSER__INPUT_DIR="/input"
RUN pip install pipenv && mkdir /txt-metaguesser && mkdir ${TXT_METAGUESSER__INPUT_DIR}
VOLUME ${TXT_METAGUESSER__INPUT_DIR}

WORKDIR /txt-metaguesser
COPY src/ /txt-metaguesser/
COPY Pipfile /txt-metaguesser/
RUN pipenv install --deploy --ignore-pipfile

ARG PLUGINS="meta_date"
ENV TXT_METAGUESSER__PLUGINS=${PLUGINS}

ENTRYPOINT ["pipenv", "run", "python3"]
CMD ["main.py"]
