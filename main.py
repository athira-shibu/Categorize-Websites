import requests
from bs4 import BeautifulSoup

with open('home.htm', 'r') as html_file:
    content = html_file.read()
    # print(content)

soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())
tags = soup.find_all('h5')
print(tags)

def scrap_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html-parser')

            #extract key data
            title = soup.title.string if soup.title else 'No title'
            body_text = ' '.join([p.text for p in soup.find_all('p')])[:500]

            return {"title": title, "text": body_text}
        else:
            return {"error": "Failed to fetch the page"}
    except Exception as e:
        return {"error": str(e)}
    
url = "https://yadhen.com/"
print(scrape_website(url))

def categorize_website(text):
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