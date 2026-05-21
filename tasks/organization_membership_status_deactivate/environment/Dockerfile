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
LABEL Description="WorkOS organization membership deactivation task: Node.js v24 + @workos-inc/node SDK pre-installed in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat > package.json <<'EOF'
{
  "name": "workos-membership-deactivate",
  "version": "1.0.0",
  "private": true,
  "description": "Deactivate a WorkOS organization membership.",
  "type": "commonjs",
  "dependencies": {
    "@workos-inc/node": "^7.0.0"
  }
}
EOF

RUN cd /home/user/myproject && npm install --no-audit --no-fund

# Container contents:
#   - ubuntu:24.04 base with curl, wget, ca-certificates, git, python3, python3-pytest, bash
#   - Node.js v24 (from NodeSource)
#   - /home/user/myproject — Node.js project with package.json
#   - @workos-inc/node SDK installed under /home/user/myproject/node_modules

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
