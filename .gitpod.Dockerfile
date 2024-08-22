FROM python:3.11-slim

# Set the working directory
WORKDIR /workspace

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install MongoDB Tooling
RUN apt-get update && \
    apt-get install -y gnupg curl && \
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt-get update && \
    apt-get install -y mongodb-clients mongodb-database-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Atlas script
COPY mongodb-utils.sh /home/gitpod/.mongodb-utils.sh
RUN chmod +x /home/gitpod/.mongodb-utils.sh && \
    echo "source /home/gitpod/.mongodb-utils.sh" >> /root/.bashrc
