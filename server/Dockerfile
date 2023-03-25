# New One
FROM python:3.11.2-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["manage.py"]