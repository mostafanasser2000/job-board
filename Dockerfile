FROM python:3.10.4-slim-bullseye

# ENV variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
# Install dependencies
RUN apt-get update && apt-get install -y netcat
COPY ./requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

# COPY project file
COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]