FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="WorkOS Pipes GitHub Integration task environment with Node.js v24 installed."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    echo "user_01EHZNVPK3SFK441A1RGBFSHRT" > user_id.txt

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Node.js SDK
#   - /home/user/myproject: base directory for the project
#   - user_id.txt containing the WorkOS User ID

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
