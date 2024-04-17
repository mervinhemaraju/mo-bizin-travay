# * Use the python alpine image container image
FROM python:3.11-alpine3.18

# * Set the working directory to /app
WORKDIR /app

# * Copy the current directory contents into the container at /app
COPY . /app

# * Dependencies for uWSGI
RUN apk add python3-dev build-base linux-headers pcre-dev && pip install -r requirements.txt && apk update

# * Create a user
RUN adduser -D th3pl4gu3

# * Run the command
ENTRYPOINT ["uwsgi", "app.ini"]
