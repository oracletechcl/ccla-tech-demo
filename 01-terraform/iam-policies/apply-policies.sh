#!/usr/bin/env bash

# Usage: ./apply-policies.sh [json_file]
# Default: policies.json
JSON_FILE="${1:-policies.json}"

oci iam policy create --from-json file://$JSON_FILE --debug



