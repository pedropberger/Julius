# Base image
FROM python:3.9-slim-buster

#set host

# Set the working directory
WORKDIR /app

# Clone the Git repository
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/pedropberger/Julius.git .

# Install dependencies
RUN pip install -r requirements.txt

# Set the command to run the main.py file
CMD ["python", "main.py"]
