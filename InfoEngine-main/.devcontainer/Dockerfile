FROM mcr.microsoft.com/devcontainers/python:3.12

# Install Node for the frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

WORKDIR /workspaces/InfoEngine
