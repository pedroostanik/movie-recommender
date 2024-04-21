FROM python:3.11-slim

ARG BASIC_AUTH_USERNAME_ARG 
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG

COPY ./requeriments.txt /usr/requeriments.txt

WORKDIR /usr

RUN pip3 install -r requeriments.txt

COPY ./src /usr/src
COPY ./models /usr/models
COPY ./data /usr/data

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py"]