FROM python:slim
ENV PYTHONUNBUFFERED 1
ENV PORT=8000

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Installing uwsgi server
RUN pip install gunicorn

COPY . /app

CMD gunicorn -b 0.0.0.0:${PORT} wsgi:app -w 2
