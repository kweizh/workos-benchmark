FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app && chmod 0755 /home/user && chmod 0755 /home/user/app

WORKDIR /home/user/app
RUN npm init -y && \
    npm install @workos-inc/node

LABEL Author="any-task-builder"
LABEL Description="WorkOS Audit Log Export task environment with Node.js v20."

# Container contents:
#   - Node.js v20 installed
#   - /home/user/app base directory initialized with npm and @workos-inc/node

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
