def retrieve_tag_text(soup, filter):
    tag = soup.select(filter)

    return tag[0].text.strip() if len(tag) > 0 else "N/A"


def retrieve_tag_href(soup, filter):
    tag = soup.select(filter)

    return tag[0]["href"] if len(tag) > 0 else "N/A"
