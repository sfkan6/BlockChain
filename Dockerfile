# The base image we want to inherit from
FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

# set work directory
WORKDIR /code
COPY . /code/

# copy project
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
