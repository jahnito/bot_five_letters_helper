FROM python:3.11.11-slim-bookworm

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/config && mkdir -p /app/db && mkdir -p /app/filters \
    && mkdir -p /app/functions && mkdir -p /app/kb && mkdir -p /app/lexicon \
    && rm requirements.txt

WORKDIR /app

COPY main.py database.db /app
COPY config /app/config
COPY db /app/db
COPY filters /app/filters
COPY functions /app/functions
COPY kb /app/kb
COPY lexicon /app/lexicon

VOLUME [ "/app/database.db" ]

ENTRYPOINT ["/usr/local/bin/python3", "main.py"]
