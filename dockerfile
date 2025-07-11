FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential libopenblas-dev

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["cosmic-reveal"]
CMD ["--depth", "1000"]
