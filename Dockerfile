# syntax=docker/dockerfile:1
# init image
FROM python:3.10-slim-buster
# create new dir
WORKDIR /app
# install dependencies
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install
# configure server
# ENV FLASK_APP=hhru_parser_async/server.py
# ENV FLASK_DEBUG=1
# run server
EXPOSE 8000
CMD ["poetry", "run", "python", "hhru_parser_async/server.py"]