FROM python:3.12-slim
RUN useradd -m appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
ENV APP_NAME=hello_world \
    APP_GREETING="helouu de aici"
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
