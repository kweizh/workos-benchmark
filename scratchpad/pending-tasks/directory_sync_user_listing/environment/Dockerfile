FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="WorkOS Directory Sync user-listing task environment: Ubuntu 24.04 + Node.js v24 + pre-installed @workos-inc/node SDK in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    printf '%s\n' \
        '{' \
        '  "name": "workos-dirsync-listing",' \
        '  "version": "1.0.0",' \
        '  "private": true,' \
        '  "description": "WorkOS Directory Sync user listing task",' \
        '  "main": "index.js"' \
        '}' > package.json && \
    npm install --no-audit --no-fund --loglevel=error @workos-inc/node@7

# Container contents:
#   - Ubuntu 24.04 base image
#   - Required system tools: curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash
#   - Node.js v24 (via NodeSource)
#   - /home/user/myproject: pre-initialized Node.js project with package.json
#   - /home/user/myproject/node_modules/@workos-inc/node: WorkOS Node SDK pre-installed (v7.x)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
