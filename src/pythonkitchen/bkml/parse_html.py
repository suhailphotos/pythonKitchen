from bs4 import BeautifulSoup
import json

def parse_bookmarks_html(html_file_path):
    """
    Parse a bookmarks HTML file and save the folder structure (with subfolders) as JSON.
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the top-level <DL> element
    top_dl = soup.find('dl', recursive=False)
    if not top_dl:
        print("No <DL> element found in the HTML file.")
        return
    dt_tag = top_dl.find_all('dt', recursive=False)
    return dt_tag

if __name__ == "__main__":
    bookmarks_file = 'bookmarks.html'
    categories = parse_bookmarks_html(bookmarks_file)
    print(categories)
