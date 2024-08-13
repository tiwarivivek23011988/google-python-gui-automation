# Use the official Python 3.12 image
FROM python:3.12-bullseye

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y wget gnupg curl unzip openjdk-11-jdk && \
    # Install Allure commandline
    curl -o allure-commandline.zip -L "https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.9/allure-commandline-2.13.9.zip" && \
    unzip allure-commandline.zip -d /opt && \
    ln -s /opt/allure-2.13.9/bin/allure /usr/bin/allure && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* allure-commandline.zip





# Set JAVA_HOME environment variableCOPY . /usr/src/app/
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Set PATH to include Java binaries# Install Python dependencies
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set working directory

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt


# Copy application files
# Default command (can be overridden by `docker-compose.yml`)
CMD ["bash", "-c", "pytest --alluredir=/usr/src/app/allure-results --cov=./tests && allure generate /usr/src/app/allure-results -o /usr/src/app/reports/allure-report && coverage html -d /usr/src/app/reports/coverage-report"]