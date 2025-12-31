# Fun Text Display Website

A simple Python web application to learn Flask basics!

## What this does:
- You type text in a box
- Click a button to display it
- Your text appears on the page

## Setup & Run:

1. **Install Flask** (if you don't have it):
   ```
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```
   python app.py
   ```

3. **Open in browser**:
   - Go to `http://localhost:5000`

## What you're learning:
- **Python basics**: Functions, decorators, imports
- **Flask framework**: Routes, templates, forms
- **HTML & CSS**: Simple frontend design
- **Client-Server**: How your browser talks to Python

## Code breakdown:

- `app.py` - Main Python file with Flask routes
  - `@app.route('/')` - Shows the form
  - `@app.route('/display')` - Handles form submission
  
- `templates/index.html` - The webpage
  - Form to submit text
  - Display area for the result

Have fun exploring! Try modifying the colors, adding more features, or experimenting with the code.

## Azure Deployment

Follow these steps to deploy this app to an existing Azure App Service.

Prerequisites:
- Azure CLI installed and configured (`az --version`)
- You are logged in (`az login --use-device-code` or `az login`)

Default values used by the included script:
- Resource group: `rg-finite-aue`
- App Service name: `finiteorg`

Quick deploy (from inside this folder):
```bash
# make the script executable (only needed once)
chmod +x deploy_to_app_service.sh

# deploy the current folder to the App Service (uses defaults)
./deploy_to_app_service.sh --src .
```

Or run from the parent folder (if you're inside `python-web`):
```bash
../deploy_to_app_service.sh --src .
```

Custom options:
```bash
./deploy_to_app_service.sh --src /path/to/app --rg myResourceGroup --app myApp --runtime "PYTHON|3.9"
```

Check live logs after deployment:
```bash
az webapp log tail --name finiteorg --resource-group rg-finite-aue
```

Notes:
- The `--src` flag points the script to the source directory to zip and deploy. Use `--src .` to deploy the current folder.
- If you prefer, keep the script executable and tracked in Git (it's included in this repo).

