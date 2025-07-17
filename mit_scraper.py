import requests
from bs4 import BeautifulSoup

class Publication:
    def __init__(self, publication, title, excerpt, pdf_text, pdf_href):
        self.publication = publication
        self.title = title
        self.excerpt = excerpt
        self.pdf_text = pdf_text
        self.pdf_href = pdf_href

    def __str__(self):
        return (
            f"Publication: {self.publication}\n"
            f"Title      : {self.title}\n"
            f"Excerpt    : {self.excerpt}\n"
            f"{self.pdf_text}: {self.pdf_href}"
        )

def get_document(url):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Hata: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("İstek hatası:", e)
        return None

def text_or_empty(el, selector):
    found = el.select_one(selector)
    return found.get_text(strip=True) if found else ""

def run():
    for i in range(1, 10):
        print(f"\n📄 SAYFA {i}\n" + "=" * 30)
        url = f"https://www.media.mit.edu/search/?page={i}&filter=publication&start_year=1979&end_year=2025&groups=%5B%5D&projects=%5B%5D&people=%5B%5D&tags=%5B%5D&_pjax=%5Bdata-pjax-pagination%5D"
        soup = get_document(url)
        if not soup:
            continue

        listings = soup.select("div.listing-content")
        publications = []

        for item in listings:
            publication = text_or_empty(item, ".module-eyebrow")
            title = text_or_empty(item, "h2.module-title")
            excerpt = text_or_empty(item, ".module-excerpt p")

            a_download = item.select_one(".download a")
            pdf_href = a_download["href"] if a_download else ""
            pdf_text = a_download.get_text(strip=True) if a_download else ""

            publications.append(Publication(publication, title, excerpt, pdf_text, pdf_href))

        for p in publications:
            print(p)
            print("–––––––––––––––––––––––––––––––")

if __name__ == "__main__":
    run()
