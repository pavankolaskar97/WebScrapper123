import requests
from bs4 import BeautifulSoup
import markdownify
import json

# Define the URL of the website to scrape
base_url = 'https://lawbriefcase.com/blogs/'
start_page = 1  # Adjust this based on the website's pagination

# Define a function to scrape individual blog pages
def scrape_blog_page(url):
    # Make an HTTP request to the blog page
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to extract title and content
        title_element = soup.find('h1', class_='post-title')
        content_element = soup.find('div', class_='post-content')

        if title_element and content_element:
            title = title_element.text.strip()
            content = content_element.decode_contents()

            # Convert HTML tables to Markdown
            content = markdownify.markdownify(content)

            return {'title': title, 'content': content}

    return None


# Define a function to scrape multiple pages
def scrape_all_pages(base_url, start_page):
    all_data = []

    # Modify the URL structure for pagination
    url = f'{base_url}?page={start_page}'

    while True:
        blog_data = scrape_blog_page(url)
        if blog_data:
            all_data.append(blog_data)
            start_page += 1
            url = f'{base_url}?page={start_page}'
        else:
            break

    return all_data

# Main execution
if __name__ == "__main__":
    scraped_data = scrape_all_pages(base_url, start_page)

    # Save the data to a JSON file
    with open('blog_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)
