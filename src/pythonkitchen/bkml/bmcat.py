import json
from bs4 import BeautifulSoup

def parse_bookmarks_html(html_file_path):
    """
    Parse the bookmarks HTML file and return a nested Python list/dict 
    structure representing the folder hierarchy only (no links).
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')


