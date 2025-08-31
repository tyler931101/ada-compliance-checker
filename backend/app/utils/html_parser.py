from bs4 import BeautifulSoup

def parse_html(html_content: str):
    """
    Parse HTML content and return a BeautifulSoup object
    """
    return BeautifulSoup(html_content, 'lxml')