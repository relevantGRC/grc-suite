FROM ubuntu:24.04

# Install conftest
USER root

RUN apt-get update && apt-get install -y gnupg software-properties-common curl

RUN cd /tmp && \
    curl -L -o conftest_0.45.0_Linux_x86_64.tar.gz https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz && \
    tar -xzf conftest_0.45.0_Linux_x86_64.tar.gz && \
    mv conftest /usr/local/bin/conftest && \
    chmod +x /usr/local/bin/conftest && \
    rm conftest_0.45.0_Linux_x86_64.tar.gz

# Install Terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && apt-get install -y terraform

USER ubuntu
