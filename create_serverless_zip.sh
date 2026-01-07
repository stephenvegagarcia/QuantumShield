#!/usr/bin/env bash
set -euo pipefail

# Create a slim deployment zip that excludes heavyweight Streamlit/quantum UI
# dependencies. The resulting archive is focused on the Flask API, which
# keeps the package small enough for serverless platforms.

OUTPUT_NAME="${1:-serverless_package.zip}"
WORKDIR="$(mktemp -d)"
cleanup() { rm -rf "$WORKDIR"; }
trap cleanup EXIT

INCLUDE_ITEMS=(
  flask_app.py
  database.py
  security_encryption.py
  cybersecurity_training.py
  file_monitor.py
  malware_detector.py
  ransomware_detector.py
  trusted_sources.py
  .env.example
  README_FLASK.md
  start_flask.sh
)

for item in "${INCLUDE_ITEMS[@]}"; do
  cp -r "$item" "$WORKDIR"/
done

cp -r templates "$WORKDIR/templates"
cp requirements-serverless.txt "$WORKDIR/requirements.txt"

pushd "$WORKDIR" > /dev/null
zip -r "$OUTPUT_NAME" . -x "__pycache__/*" "*.pyc"
popd > /dev/null

mv "$WORKDIR/$OUTPUT_NAME" "./$OUTPUT_NAME"
echo "Created $OUTPUT_NAME (serverless-focused Flask bundle)"
