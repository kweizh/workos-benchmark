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
LABEL Description="Node.js Express app with WorkOS SDK installed, missing MFA routes."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    npm init -y && \
    npm install express @workos-inc/node && \
    cat > server.js <<'EOF'
const express = require("express");
const { WorkOS } = require("@workos-inc/node");

const app = express();
app.use(express.json());

const workos = new WorkOS(process.env.WORKOS_API_KEY);

app.get("/", (req, res) => {
  res.send("Hello World");
});

// TODO: Implement /enroll, /challenge, and /verify endpoints here.

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/app - Express project with @workos-inc/node installed.
#   - /home/user/app/server.js - Basic Express server without MFA routes.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
