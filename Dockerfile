FROM python:3.11-slim

ARG BASIC_AUTH_USERNAME_ARG 
ARG BASIC_AUTH_PASSWORD_ARG
ARG DB_USER_ARG
ARG DB_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG
ENV DB_USER=$DB_USER_ARG
ENV DB_PASSWORD=$DB_PASSWORD_ARG

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

RUN pip3 install scikit-surprise
RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models
COPY ./data /usr/data

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py"]