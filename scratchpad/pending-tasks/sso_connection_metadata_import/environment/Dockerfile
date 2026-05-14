FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user
RUN mkdir -p /home/user/myproject && chmod 0755 /home/user/myproject

# Pre-warm the @workos-inc/node SDK in a global npm cache location so the
# agent's `npm install @workos-inc/node` is fast and works offline-friendly.
RUN npm install -g @workos-inc/node

LABEL Author="any-task-builder"
LABEL Description="WorkOS Admin Portal SSO Portal-link task environment: Ubuntu 24.04 + Node.js v24 + @workos-inc/node SDK."

# Container contents:
#   - Ubuntu 24.04 base
#   - System packages: curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash
#   - Node.js v24 (from NodeSource) and npm
#   - Globally installed @workos-inc/node SDK (so the agent can install it locally without surprises)
#   - /home/user/myproject — empty project directory for the agent to scaffold

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
