# Using official python runtime base image
FROM python:3.11.4-alpine3.18

# Set the working directory in docker
WORKDIR /app

# Copy everything from the current directory to the working dir in docker
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "./grab.py" ]
