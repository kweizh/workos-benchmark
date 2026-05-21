FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    pip3 install --break-system-packages pytest-json-ctrf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat > package.json <<'EOF'
{
  "name": "email_verification_send",
  "version": "1.0.0",
  "private": true,
  "description": "Send a verification email to an existing WorkOS user.",
  "type": "commonjs",
  "dependencies": {
    "@workos-inc/node": "^7.0.0"
  }
}
EOF

RUN cd /home/user/myproject && npm install --no-audit --no-fund

LABEL Author="generate-harbor-tasks"
LABEL Description="Send a verification email to an existing WorkOS user."

# Container contents:
#   - ubuntu:24.04 base with curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash, ripgrep
#   - pip3 packages: pytest-json-ctrf
#   - Node.js v24 (from NodeSource)
#   - /home/user/myproject - Node.js project with @workos-inc/node SDK installed

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
