import datefinder


def retrieve_date(soup, filter):
    tag = soup.select(filter)

    if len(tag) > 0:
        texts = "".join(tag[0].text.splitlines()).split()

        for text in texts:
            dates = list(datefinder.find_dates(text))

            if len(dates) > 0:
                return dates[0].strftime("%Y-%m-%d")

    return "N/A"


def retrieve_tag_text(soup, filter):
    tag = soup.select(filter)
    return tag[0].text.strip() if len(tag) > 0 else "N/A"


def retrieve_tag_href(soup, filter):
    tag = soup.select(filter)

    return tag[0]["href"] if len(tag) > 0 else "N/A"
