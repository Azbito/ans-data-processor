import requests
from bs4 import BeautifulSoup


def get_pdf_links(target_url: str):

    response = requests.get(target_url)

    if response.status_code != 200:
        raise Exception(f"Falha ao acessar a página: {target_url}")

    soup = BeautifulSoup(response.text, "html.parser")

    pdf_links = [
        link["href"]
        for link in soup.find_all("a", href=True)
        if "Anexo" in link["href"] and link["href"].endswith(".pdf")
    ]

    if not pdf_links:
        raise Exception(f"There's no PDF URL for: {target_url}")

    return pdf_links
