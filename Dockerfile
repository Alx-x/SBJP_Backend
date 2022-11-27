FROM python:3.9.15-slim-buster
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app" ]