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
LABEL Description="WorkOS passwordless email OTP (Magic Auth) Node.js v24 task environment with a pre-initialized myproject scaffold."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "workos-passwordless-otp",
  "version": "1.0.0",
  "private": true,
  "description": "Passwordless email OTP (Magic Auth) demo using the WorkOS Node SDK.",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {}
}
EOF

# Container contents:
#   - Ubuntu 24.04 base with curl, wget, git, python3, python3-pytest, bash
#   - Node.js v24 (via NodeSource) and npm for installing @workos-inc/node
#   - /home/user/myproject pre-seeded with a minimal package.json (no SDK installed yet)
#   - The agent must install @workos-inc/node and implement index.js to call the
#     live WorkOS Magic Auth (passwordless email OTP) API.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
