FROM python:3.9.15-slim-buster
ARG PORT
ARG DATABASE_URL
ARG SECRET_KEY
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "gunicorn", '-b', ':$(PORT)', "wsgi:app"]