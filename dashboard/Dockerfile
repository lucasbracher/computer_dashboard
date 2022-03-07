# Use an official Python runtime as a parent image
FROM ubuntu

# Set the working directory to /app
WORKDIR /dashboard/

# Copy the current directory contents into the container in the workdir
COPY . .

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
    apt-get install -y nodejs npm
RUN npm install -g @vue/cli
RUN cd /dashboard && npm install


