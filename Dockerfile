# Base image
FROM python:3.8.10
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["app.py"]