FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment with the @workos-inc/node SDK pre-installed in /home/user/myproject for WorkOS organization membership role assignment tasks."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "private": true,
  "description": "WorkOS organization membership role assignment script.",
  "main": "index.js",
  "dependencies": {
    "@workos-inc/node": "^7.0.0"
  }
}
EOF

RUN cd /home/user/myproject && npm install --no-audit --no-fund

# Container contents:
#   - Ubuntu 24.04 base
#   - System packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash gnupg
#   - Node.js v24 (installed via NodeSource)
#   - /home/user/myproject  — scaffolded Node.js project with package.json
#   - @workos-inc/node SDK installed in /home/user/myproject/node_modules

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
