# Base image
FROM python:3.8.10

# Set working directory
WORKDIR /app

# Copy files
COPY app.py /appS
COPY requirements.txt /app
COPY models /app/models

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "120"]
CMD ["app:app"]