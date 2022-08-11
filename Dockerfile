FROM python:3.8-slim

ENV WORKERS=3
ENV USER=django
ENV PATH=${PATH}:/home/${USER}/.local/bin
ENV PORT=80

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

# Fixing files & folders permissions
RUN chown ${USER}:${USER} /app/db.sqlite3 \
	&& chmod 664 /app/db.sqlite3

VOLUME ["/app"]

EXPOSE ${PORT}

HEALTHCHECK --interval=15s --timeout=14s --start-period=5s CMD curl -fsSLI http://127.0.0.1:${PORT}/admin/login/ | grep -q "200 OK" || false

CMD gunicorn --bind 0.0.0.0:${PORT} -w ${WORKERS} app.wsgi
