FROM python:3.8-slim

ENV WORKERS=3
ENV USER=django
ENV PATH=${PATH}:/home/${USER}/.local/bin

EXPOSE 80

WORKDIR /app

#RUN apt-get update && apt-get install -y gunicorn \
#	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# create a django user & switch to it.
RUN useradd -m ${USER} && chown ${USER}:${USER} /app
USER ${USER}

COPY requirements.txt ./

# install django requirements.
RUN pip3 install -r requirements.txt --no-cache-dir

# copy all django files.
COPY --chown=${USER}:${USER} . .

# applying migrations
RUN python3 manage.py migrate && python3 manage.py collectstatic --no-input --skip-checks

VOLUME ["/app"]

CMD gunicorn --bind 0.0.0.0:80 -w ${WORKERS} app.wsgi
#CMD python3 manage.py runserver 0.0.0.0:80
