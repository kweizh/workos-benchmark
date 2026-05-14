FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user /home/user/project

# Mock amika CLI since we assume it is available
RUN echo '#!/bin/bash\nexit 0' > /usr/local/bin/amika && chmod +x /usr/local/bin/amika

LABEL Author="any-task-builder"
LABEL Description="Node.js environment for WorkOS User Management API task"

# Container contents:
#   - Node.js v24 installed
#   - /home/user/project directory created
#   - amika CLI available in PATH

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
