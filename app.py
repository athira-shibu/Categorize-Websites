import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Function to scrape website content
def scrape_website(url):
    """Fetches and extracts text from a given website URL."""
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url 
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title"
            body_text = ' '.join([p.text for p in soup.find_all('p')])[:500]  # Limit text length
            return {"title": title, "text": body_text}
        else:
            return {"error": "Failed to fetch the page"}
    except Exception as e:
        return {"error": str(e)}

# Function to categorize the website
def categorize_website(text):
    """Categorizes the website based on keywords in the text."""
    categories = {
        "Contractors": ["construction", "building", "contractor"],
        "Architects": ["architecture", "design", "blueprint"],
        "Suppliers": ["materials", "supplier", "concrete"]
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text.lower():
                return category
    return "Unknown"

# HTML Template for the web UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Construction Website Categorizer</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        input { padding: 10px; width: 300px; margin: 10px; }
        button { padding: 10px 20px; }
        h3 { color: green; }
    </style>
</head>
<body>
    <h2>Enter a website URL:</h2>
    <form method="post">
        <input type="text" name="url" placeholder="https://example.com" required>
        <button type="submit">Categorize</button>
    </form>
    {% if category %}
        <h3>Category: {{ category }}</h3>
    {% endif %}
    {% if error_message %}
    <p style="color: red;">Error: {{ error_message }}</p>
    {% endif %}
</body>
</html>
"""

# Flask route to handle the form submission
@app.route("/", methods=["GET", "POST"])
def index():
    category = None
    error_message = None

    if request.method == "POST":
        url = request.form.get("url")
        print(f"Received URL: {url}")  # Debugging print

        data = scrape_website(url)
        print(f"Scraped Data: {data}")  # Debugging print

        if "error" in data:
            error_message = data["error"]
            print(f"Error Message: {error_message}")  # Debugging print
        else:
            category = categorize_website(data["text"])
            print(f"Categorized as: {category}")  # Debugging print
    
    return render_template_string(HTML_TEMPLATE, category=category, error_message=error_message)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
