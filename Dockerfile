FROM python:3.9.15-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0$PORT", "wsgi:app" ]