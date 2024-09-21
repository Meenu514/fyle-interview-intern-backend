FROM python:3.8-slim-bookworm

RUN mkdir -p /home/app

RUN useradd app

ENV HOME=/home/app
ENV APP_HOME=/home/app/fyle-backend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip

COPY . $APP_HOME

RUN pip install --no-cache -r requirements.txt

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["/home/app/fyle-backend/run.sh"]