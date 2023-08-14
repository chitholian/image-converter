# Simple Image Converter Microservice

A very simple microservice to convert between image formats and resize.

## Basic Requirements

- **Python** `3.10+`
- **pip**
- **virtualenv**

### For Containerization

- Podman
- Docker

## Create Python Virtual Environment

```sh
virtualenv .venv
source .venv/bin/activate
```

## Install Required Packages

```sh
pip install -r requirements.txt
```

## Run WSGI Server

```sh
cd src/
gunicorn image_converter:app run 
```

Now, you can browse http://127.0.0.1:8000 to view and test API documentation in Swagger.

## Build Container Image

### Using Podman

```sh
podman build -t image-converter .
```

Run the built container image:

```sh
podman run --rm -d -p 8000:8000 localhost/image-converter:latest
```

### Using Docker

```sh
docker build -t image-converter .
```

Run the built container image:

```sh
docker run --rm -d -p 8000:8000 localhost/image-converter:latest
```

## Demo Credentials

Following credentials can be used for HTTP Basic Auth for testing:

- Username: `cns_demo`
- Password: `cns_demo`