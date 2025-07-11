#!/bin/sh
set -e

# Create new .streamlit directory
mkdir -p /app/.streamlit

# Create skeleton for secrets.toml file
cat <<EOF > /app/.streamlit/secrets.toml
[general]
blob_connection_string = "${BLOB_CONNECTION_STRING:-}"

[auth]
redirect_uri = "${REDIRECT_URI:-}"
cookie_secret = "${COOKIE_SECRET:-}"

[auth.auth0]
domain = "${AUTH0_DOMAIN:-}"
client_id = "${AUTH0_CLIENT_ID:-}"
client_secret = "${AUTH0_CLIENT_SECRET:-}"
server_metadata_url = "${AUTH0_SERVER_METADATA_URL:-}"
EOF

# Spin up streamlit application following secrets.toml generation
exec streamlit run frontend/main.py --server.port "${PORT:-8501}"