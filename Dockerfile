FROM python:3.13-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install AWS CLI and clean up
RUN apt-get update && \
    apt-get install -y awscli && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Start the app
CMD ["python3", "app.py"]
