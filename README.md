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
