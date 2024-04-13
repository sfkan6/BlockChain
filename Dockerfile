FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD ["uvicorn",  "main:app", "--host", "0.0.0.0"]
