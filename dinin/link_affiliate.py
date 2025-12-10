from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class LinkAffiliate:
    def __init__(
        self,
        amazon_tag: str | None = None,
    ):
        self.amazon_tag = amazon_tag

    def affiliate_link(self, url: str) -> str:
        if url.startswith("https://www.amazon.it/") and self.amazon_tag is not None:
            return self.affiliate_link_amazon(url)
        return url  # No affiliate link available for this URL

    def affiliate_link_amazon(self, url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params["tag"] = [self.amazon_tag]
        new_query = urlencode(query_params, doseq=True)
        new_url = parsed_url._replace(query=new_query)
        return urlunparse(new_url)
