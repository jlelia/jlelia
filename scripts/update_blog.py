import cloudscraper
from bs4 import BeautifulSoup
import re
import sys

def update_readme():
    url = "https://jlelia.net/blog"

    # Create a scraper that mimics a real Chrome browser
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    
    try:
        response = scraper.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching blog: {e}")
        sys.exit(1)

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get only the newest 3 blog cards
    cards = soup.select(".cards .card")[:3] 
    
    blog_overview = ""
    
    for card in cards:
        link = card.get('href')
        if link.startswith('/'):
            link = f"https://jlelia.net{link}"
            
        title = card.find('h3').text.strip()
        date = card.find('h4').text.strip()
        
        blog_overview += f"- [{title}]({link}) - *{date}*\n"

    # Update README
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as file:
        readme = file.read()

    # Regex to capture the start tag, content, and end tag
    pattern = r"(<!-- BLOG-POST-LIST:START -->)(.*?)(<!-- BLOG-POST-LIST:END -->)"

    replacement = f"\\1\n{blog_overview}\\3"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(new_readme)
        
    print("README updated successfully.")

if __name__ == "__main__":
    update_readme()
