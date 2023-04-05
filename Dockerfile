FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app/. .

#ENV FLASK_APP=main.py
ENV PYTHONPATH=/app

EXPOSE 9000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:9000"]
