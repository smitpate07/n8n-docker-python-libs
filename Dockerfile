# Use the official n8n base image
FROM n8nio/n8n:latest

# Switch to the root user to install system packages
USER root

# Install Python 3 and pip using the Alpine package manager (apk)
RUN apk add --update python3 py3-pip

USER node
# Copy your requirements.txt file into the container
COPY requirements.txt /tmp/requirements.txt
COPY n_test.py /tmp/n_test.py

# Install the Python libraries listed in requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt --break-system-packages





