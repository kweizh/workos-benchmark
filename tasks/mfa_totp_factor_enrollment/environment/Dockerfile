FROM --platform=linux/amd64 ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment with the @workos-inc/node SDK pre-installed in /home/user/myproject for the WorkOS MFA TOTP factor enrollment task."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    printf '%s\n' '{' \
                  '  "name": "mfa-totp-factor-enrollment",' \
                  '  "version": "1.0.0",' \
                  '  "private": true,' \
                  '  "type": "commonjs",' \
                  '  "dependencies": {' \
                  '    "@workos-inc/node": "^7.0.0"' \
                  '  }' \
                  '}' > package.json && \
    npm install --no-audit --no-fund --loglevel=error

# Container contents:
#   - Ubuntu 24.04 base with curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash
#   - Node.js v24 (via NodeSource setup_24.x)
#   - /home/user                       — task home base directory
#   - /home/user/myproject             — pre-initialized Node.js project
#   - /home/user/myproject/package.json — declares @workos-inc/node as a dependency
#   - /home/user/myproject/node_modules — @workos-inc/node SDK installed and ready to use

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
