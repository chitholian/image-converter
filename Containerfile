FROM python:3.11-alpine

COPY ./src /opt/app
COPY ./requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN apk update && apk add python3-dev gcc libffi-dev libc-dev
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "image_converter:app"]
