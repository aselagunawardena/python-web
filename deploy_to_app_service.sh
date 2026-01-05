#!/usr/bin/env bash
set -euo pipefail

# Simple deploy helper: zips a folder and deploys via `az webapp deployment source config-zip`
# Usage: ./deploy_to_app_service.sh --src . --rg rg-finite-aue --app finiteorg

SRC="."
RG="rg-finite-aue"
APP="finiteorg"
RUNTIME="PYTHON|3.9"

print_usage() {
  echo "Usage: $0 [--src PATH] [--rg RESOURCE_GROUP] [--app APP_NAME] [--runtime RUNTIME]"
  exit 1
}

# parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --src)
      SRC="$2"; shift 2;;
    --rg)
      RG="$2"; shift 2;;
    --app)
      APP="$2"; shift 2;;
    --runtime)
      RUNTIME="$2"; shift 2;;
    -h|--help)
      print_usage;;
    *)
      echo "Unknown argument: $1"; print_usage;;
  esac
done

if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLI 'az' not found. Install it and login (az login)."
  exit 2
fi

echo "Preparing zip from: $SRC"
TMPZIP="/tmp/deploy_$(date +%s).zip"
# create zip, excluding typical venv/git files
(cd "$SRC" && zip -r "$TMPZIP" . -x "*.pyc" "__pycache__/*" "*.git*" "venv/*" "env/*" "node_modules/*")

echo "Deploying $TMPZIP to App Service '$APP' in resource group '$RG'..."
az webapp deployment source config-zip --resource-group "$RG" --name "$APP" --src "$TMPZIP"

echo "Deployment command finished. Remove temp file: $TMPZIP"

exit 0
