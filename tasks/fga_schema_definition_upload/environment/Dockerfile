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
LABEL Description="WorkOS FGA schema upload task: Node.js v24 + @workos-inc/node SDK pre-installed in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "fga-schema-definition-upload",
  "version": "1.0.0",
  "private": true,
  "description": "Scaffold for the WorkOS FGA resource-type schema upload task.",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "@workos-inc/node": "^7.61.0"
  }
}
EOF

RUN cd /home/user/myproject && npm install --silent --no-audit --no-fund

# Container contents:
#   - Ubuntu 24.04 base.
#   - System libs: curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash.
#   - Node.js v24 (via NodeSource) and bundled npm — provides native fetch() for REST calls.
#   - /home/user/myproject scaffold containing package.json with @workos-inc/node installed in node_modules.
#   - No index.js or schema.json — the agent must create them.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
