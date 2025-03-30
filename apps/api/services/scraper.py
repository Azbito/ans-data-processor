import requests
from bs4 import BeautifulSoup
from typing import List


class ScraperService:
    @staticmethod
    def get_pdf_links(target_url: str) -> List[str]:
        try:
            response = requests.get(target_url)

            if response.status_code != 200:
                raise Exception(f"Error while accessing: {target_url}")

            
            content = response.text if hasattr(response, 'text') else response.content.decode('utf-8')
            soup = BeautifulSoup(content, "html.parser")

            pdf_links = [
                link["href"]
                for link in soup.find_all("a", href=True)
                if "Anexo" in link["href"] and link["href"].endswith(".pdf")
            ]

            if not pdf_links:
                raise Exception(f"There's no PDF URL for: {target_url}")

            return pdf_links
        except Exception as e:
            raise Exception(f"Failed to get PDF links: {str(e)}")
