import requests
from bs4 import BeautifulSoup
import re
import sys

def update_readme():
    # Fetch blog hub from my personal website
    url = "https://jlelia.net/blog"
    # User-Agent header to prevent 403 Forbidden errors
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching blog: {e}")
        sys.exit(1)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # /blog has the following for each blog page: <div class="cards"> -> <a class="card">
    cards = soup.select(".cards .card")[:3] # Get only the newest 3

    # Create empty holder for blog overviews
    blog_overview = ""
    
    for card in cards:
        # Extract relative link in each card and make absolute
        link = card.get('href')
        if link.startswith('/'):
            link = f"https://jlelia.net{link}"
            
        # Extract title (h3) and date (h4) from each card
        title = card.find('h3').text.strip()
        date = card.find('h4').text.strip()
        
        # Format as a Markdown list item for the README
        blog_overview += f"- [{title}]({link}) - *{date}*\n"

    # Update jlelia README.md
    readme_path = "README.md"
    
    with open(readme_path, "r", encoding="utf-8") as file:
        readme = file.read()

    # Regex to capture the start tag, content, and end tag
    pattern = r"()(.*?)()"
    
    # We replace the middle group (content) with our new blog_overview
    replacement = f"\\1\n{blog_overview}\\3"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_readme)
        
    print("README updated successfully.")

if __name__ == "__main__":
    update_readme()
