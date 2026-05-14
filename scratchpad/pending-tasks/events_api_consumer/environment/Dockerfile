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
LABEL Description="WorkOS Events API consumer task environment with Node.js v24 and the @workos-inc/node SDK pre-staged."

# Pre-create the empty project directory so the agent has somewhere to scaffold the script.
RUN mkdir -p /home/user/myproject

# Warm up an npm cache copy of the WorkOS SDK so `npm install @workos-inc/node` is fast at task time.
RUN mkdir -p /opt/workos-cache && \
    cd /opt/workos-cache && \
    npm init -y >/dev/null && \
    npm install --no-audit --no-fund @workos-inc/node && \
    rm -rf /opt/workos-cache/node_modules /opt/workos-cache/package-lock.json /opt/workos-cache/package.json

# Container contents:
#   - Ubuntu 24.04 base
#   - System tools: curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash
#   - Node.js v24 (and bundled npm) for running the WorkOS Events API consumer script
#   - /home/user/myproject — empty project directory pre-created for the agent
#   - npm cache pre-populated with @workos-inc/node to speed up subsequent installs

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
