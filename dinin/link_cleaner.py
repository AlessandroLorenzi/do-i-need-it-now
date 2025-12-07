# TODO: this is a test, not connected to anything yet
import re


class LinkCleaner:
    def clean(self, link: str) -> str:
        link = self.amazon(link)
        return link
    
    def amazon(self, link: str) -> str:
        regex = r"(https?://)?(www\.)?amazon\.([a-z]{2,3})(\.[a-z]{2})?/"
        url_match = re.match(regex, link)
        if not url_match:
            return link
        
        asin = re.search(r"/dp/([A-Z0-9]{10})", link)
        if not asin:
            return link
        
        link = url_match.group(0) + "dp/" + asin.group(1)

        return link

if __name__ == "__main__":
    cleaner = LinkCleaner()
    test_link = "https://www.amazon.it/DALSTRONG-Nakiri-Knife-High-Carbon-Pakkawood/dp/B076G6PC36/?_encoding=UTF8&pd_rd_w=jHLDF&content-id=amzn1.sym.b4434d57-8aaf-4606-a7d8-4a94c430d33e%3Aamzn1.symc.b1464ab7-6d6a-4fc8-be8f-f2e9bcc64228&pf_rd_p=b4434d57-8aaf-4606-a7d8-4a94c430d33e&pf_rd_r=Q95YJ2HJ4FPGGQ7N8FGE&pd_rd_wg=IaEtG&pd_rd_r=b3c71f7d-1401-4c2c-92af-9ddf2477c452&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d&th=1"
    cleaned_link = cleaner.clean(test_link)
    print(f"Original link: {test_link}")
    print(f"Cleaned link: {cleaned_link}")