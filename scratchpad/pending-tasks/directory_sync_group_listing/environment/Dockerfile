FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment with @workos-inc/node SDK installed in /home/user/myproject for WorkOS Directory Sync group listing."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    npm init -y && \
    npm install @workos-inc/node

# Container contents:
#   - Ubuntu 24.04 base
#   - Node.js v24 + npm
#   - /home/user/myproject: Node.js project pre-initialized with @workos-inc/node dependency
#   - Python 3 + pytest for state verification

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
