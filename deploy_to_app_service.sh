#!/usr/bin/env bash
set -euo pipefail

# deploy_to_app_service.sh
# Usage: ./deploy_to_app_service.sh [--src PATH] [--rg RG] [--app NAME] [--runtime PYTHON|3.9]
# Defaults: --src ./python-web --rg rg-finite-aue --app finiteorg

SRC_DIR="./python-web"
RG="rg-finite-aue"
APP="finiteorg"
RUNTIME="" # optional, e.g. "PYTHON|3.9"

print_usage() {
  cat <<EOF
Usage: $0 [--src PATH] [--rg RG] [--app NAME] [--runtime RUNTIME] [--no-restart]

Defaults:
  --src ./python-web
  --rg rg-finite-aue
  --app finiteorg

Examples:
  $0
  $0 --src ./python-web --rg my-rg --app my-app --runtime "PYTHON|3.9"
EOF
}

NO_RESTART=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --src) SRC_DIR="$2"; shift 2;;
    --rg) RG="$2"; shift 2;;
    --app) APP="$2"; shift 2;;
    --runtime) RUNTIME="$2"; shift 2;;
    --no-restart) NO_RESTART=1; shift 1;;
    -h|--help) print_usage; exit 0;;
    *) echo "Unknown arg: $1"; print_usage; exit 2;;
  esac
done

if ! command -v az >/dev/null 2>&1; then
  echo "az CLI not found. Install Azure CLI first." >&2
  exit 3
fi

echo "Checking Azure login..."
if ! az account show >/dev/null 2>&1; then
  echo "You're not logged in. Opening device login..."
  az login --use-device-code
fi

echo "Verifying resource group '$RG'..."
if ! az group show --name "$RG" >/dev/null 2>&1; then
  echo "Resource group '$RG' not found." >&2
  exit 4
fi

echo "Verifying App Service '$APP' in RG '$RG'..."
if ! az webapp show --name "$APP" --resource-group "$RG" >/dev/null 2>&1; then
  echo "App Service '$APP' not found in resource group '$RG'." >&2
  exit 5
fi

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Source directory '$SRC_DIR' does not exist." >&2
  exit 6
fi

TMP_ZIP=$(mktemp -t webapp-deploy-XXX).zip
echo "Creating zip archive $TMP_ZIP from $SRC_DIR..."
(
  cd "$SRC_DIR"
  zip -r "$TMP_ZIP" . -x "*.pyc" "__pycache__/*" ".git/*" "venv/*" "node_modules/*" >/dev/null
)

echo "Deploying to App Service '$APP'..."
if az webapp deploy --resource-group "$RG" --name "$APP" --src-path "$TMP_ZIP" >/dev/null 2>&1; then
  echo "Deployment started with 'az webapp deploy'."
else
  echo "Falling back to 'az webapp deployment source config-zip'..."
  az webapp deployment source config-zip --resource-group "$RG" --name "$APP" --src "$TMP_ZIP"
fi

if [[ -n "$RUNTIME" ]]; then
  echo "Setting runtime to $RUNTIME"
  az webapp config set --resource-group "$RG" --name "$APP" --linux-fx-version "$RUNTIME"
fi

if [[ "$NO_RESTART" -eq 0 ]]; then
  echo "Restarting App Service..."
  az webapp restart --resource-group "$RG" --name "$APP"
fi

echo "Cleaning up..."
rm -f "$TMP_ZIP"

echo "Deployment finished. Check logs with: az webapp log tail --name $APP --resource-group $RG"
