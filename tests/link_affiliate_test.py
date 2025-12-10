from dinin.link_affiliate import LinkAffiliate


def test_link_affiliate():
    la = LinkAffiliate(amazon_tag="testtag-20")

    assert (
        la.affiliate_link("https://www.amazon.it/dp/B0DTRWD3MT/?_encoding=UTF8")
        == "https://www.amazon.it/dp/B0DTRWD3MT/?_encoding=UTF8&tag=testtag-20"
    )

    assert (
        la.affiliate_link("https://www.amazon.it/dp/B0DTRWD3MT/")
        == "https://www.amazon.it/dp/B0DTRWD3MT/?tag=testtag-20"
    )


def test_link_affiliate_existing_tag():
    la = LinkAffiliate(amazon_tag="newtag-20")

    assert (
        la.affiliate_link(
            "https://www.amazon.it/dp/B0DTRWD3MT/?tag=oldtag-20&_encoding=UTF8"
        )
        == "https://www.amazon.it/dp/B0DTRWD3MT/?tag=newtag-20&_encoding=UTF8"
    )


def test_link_affiliate_non_amazon():
    la = LinkAffiliate(amazon_tag="testtag-20")

    assert (
        la.affiliate_link("https://www.example.com/product")
        == "https://www.example.com/product"
    )
