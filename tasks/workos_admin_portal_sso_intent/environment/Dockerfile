FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user/project

# Dummy amika CLI to satisfy the validation requirement during local testing
RUN echo '#!/bin/bash\nif [ "$1" == "validate" ]; then\n  if [ -f "$2" ]; then\n    exit 0\n  else\n    echo "File not found"\n    exit 1\n  fi\nfi\nexit 1\n' > /usr/local/bin/amika && \
    chmod +x /usr/local/bin/amika

LABEL Author="any-task-builder"
LABEL Description="WorkOS Admin Portal SSO Intent task environment with Node.js"

# Container contents:
#   - Node.js installed for the WorkOS Node SDK.
#   - /home/user/project - empty project directory for the task.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
