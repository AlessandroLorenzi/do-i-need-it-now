import requests
from bs4 import BeautifulSoup


class OpenGraphInfoFetcher:
    def fetch(self, url: str) -> dict:
        if url == "":
            return {}

        if "amazon." in url:
            return self.fetch_amazon(url)
        else:
            return self.fetch_default(url)

    def fetch_default(self, url: str) -> dict:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        og_data = {}
        for tag in soup.find_all("meta"):
            prop = tag.get("property")
            if prop and prop.startswith("og:"):
                og_data[prop[3:]] = tag.get("content")
        print(og_data)
        return og_data

    def fetch_amazon(self, url: str) -> dict:
        og_data = {}
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        image_tag = soup.find("img", {"id": "landingImage"})

        if image_tag:
            og_data["image"] = image_tag.get("src", "")

        return og_data
