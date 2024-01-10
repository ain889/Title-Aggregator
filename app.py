import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.theverge.com/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the relevant information (headlines, article URLs, and publication time)
    articles = soup.find_all('h2', class_='mb-8 font-polysans text-30 font-bold leading-100 sm:text-35')
    headlines = [article.text.strip() for article in articles]

    links = soup.find_all('a', class_='after:absolute after:inset-0 group-hover:shadow-highlight-franklin dark:group-hover:shadow-highlight-blurple')
    article_urls = [link['href'] for link in links]

    times = soup.find_all('div', class_='inline-block text-gray-63 dark:text-gray-94')
    publication_times = [time.text.strip() for time in times]

    # Combine headlines, article URLs, and publication times into a list of tuples
    articles_data = list(zip(headlines, article_urls, publication_times))

    # Sort the list of tuples based on publication times
    articles_data.sort(key=lambda x: datetime.strptime(x[2].replace('ago', '').strip(), '%b %d, %Y %I:%M %p'))

    # Create a simple HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Verge Headlines</title>
    </head>
    <body>
        <h1>The Verge Headlines (Since January 1, 2022)</h1>
        <ul>
    """

    # Add clickable headlines and sorted publication times to the HTML template
    for headline, article_url, publication_time in articles_data:
        html_template += f"<li><a href='{article_url}' target='_blank'>{headline}</a> - Published at {publication_time}</li>"

    # Close HTML tags
    html_template += """
        </ul>
    </body>
    </html>
    """

    # Write the HTML content to the index.html file
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html_template)

    print("Scraped data has been saved to index.html.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
