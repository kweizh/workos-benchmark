FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        postgresql postgresql-contrib postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Assuming amika is a CLI tool that needs to be globally available, we mock it here 
# so that the build does not fail. If it's provided by the testing environment, 
# this mock won't interfere if it's placed in a lower priority path or overwritten.
RUN echo '#!/bin/bash\necho "amika mock"\nexit 0' > /usr/local/bin/amika && \
    chmod +x /usr/local/bin/amika

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="WorkOS Directory Sync Webhook task environment with Node.js and PostgreSQL."

# Setup PostgreSQL DB and user
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER testuser WITH SUPERUSER PASSWORD 'testpass';" && \
    createdb -O testuser testdb
USER root

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    npm init -y && \
    npm install express pg @workos-inc/node

RUN cat >/home/user/app/init_db.js <<'EOF'
const { Client } = require('pg');
const client = new Client({ connectionString: process.env.DATABASE_URL });
async function init() {
  await client.connect();
  await client.query(`
    CREATE TABLE IF NOT EXISTS users (
      id VARCHAR(255) PRIMARY KEY,
      email VARCHAR(255),
      first_name VARCHAR(255),
      last_name VARCHAR(255),
      state VARCHAR(50)
    );
  `);
  await client.end();
}
init();
EOF

# Container contents:
#   - Node.js v24 for the app
#   - PostgreSQL for the database
#   - /home/user/app: base directory for the project

CMD ["/bin/bash", "-c", "trap : TERM INT; service postgresql start; sleep infinity & wait"]
