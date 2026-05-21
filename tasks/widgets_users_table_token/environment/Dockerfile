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
LABEL Description="WorkOS Widgets API task environment: Node.js v24 + @workos-inc/node SDK pre-installed in /home/user/myproject."

# Pre-create the project directory and install the WorkOS Node SDK so the
# initial environment matches the task's stated starting state.
RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    npm init -y >/dev/null && \
    npm install @workos-inc/node

# Container contents:
#   - Base: ubuntu:24.04
#   - System tools: curl, wget, ca-certificates, git, python3, python3-pip, python3-pytest, bash
#   - Node.js v24 (via NodeSource)
#   - /home/user/myproject pre-initialized with @workos-inc/node installed
#   - The user is expected to add generate_token.js, run it, and produce widget_token.txt

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
