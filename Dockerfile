FROM python:3.7-alpine 
# 
LABEL Mcuve WorkOutTracker

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# this ones we don't removed after installed
RUN apk add --update --no-cache postgresql-client jpeg-dev



# install the apk for the postgres client witout unessesary cache
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
#  this are temporarly requirements for installing postgresql

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app

WORKDIR /app

COPY ./app /app

# this way we can set a fold that contains all the images, therefor we can share across containers
# -p stands for creating the folders if not exsits
RUN mkdir -p /vol/web/media 

RUN mkdir -p /vol/web/static

RUN adduser -D user
# create a user for running our process

# sets the owner ship to all the subdirectorys of the vol folder to the custom user
# -R stands for recursive for all subdirectorys
RUN chown -R user:user /vol/

# sets permissions to  the user that can read and write
RUN chmod -R 755 /vol/web

USER user
# switch to the user