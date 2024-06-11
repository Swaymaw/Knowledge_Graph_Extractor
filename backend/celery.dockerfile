FROM python:3.10

WORKDIR /

COPY . ./

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y
RUN apt-get install gcc -y
RUN apt-get install -y
RUN pip install --upgrade pip
RUN pip install --timeout=1000 --no-cache-dir -r /requirements.txt
RUN python -m spacy download en
RUN python -m nltk.downloader stopwords

CMD celery -A task worker --concurrency=1 --pool=solo
