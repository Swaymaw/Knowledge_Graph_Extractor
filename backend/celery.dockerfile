FROM python:3.10

WORKDIR /

COPY . ./

RUN apt-get update && apt-get install -y
RUN apt-get install gcc -y
RUN apt-get install -y
RUN pip install --upgrade pip
RUN pip install --timeout=1000 --no-cache-dir -r /requirements.txt
RUN python -m spacy download en

RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get install -y ant && \
    apt-get clean;

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

CMD celery -A task worker --concurrency=1 --pool=solo

