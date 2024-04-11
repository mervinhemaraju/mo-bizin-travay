import datefinder


def retrieve_date(soup, filter):
    tag = soup.select(filter)

    if len(tag) > 0:
        text = tag[0].text.strip()

        dates = list(datefinder.find_dates(text))

        if len(dates) > 0:
            return dates[0]

    return None


def retrieve_tag_text(soup, filter):
    tag = soup.select(filter)

    return tag[0].get_text(strip=True).strip() if len(tag) > 0 else "N/A"


def retrieve_tag_href(soup, filter):
    tag = soup.select(filter)

    return tag[0].get("href", None) if len(tag) > 0 else None
