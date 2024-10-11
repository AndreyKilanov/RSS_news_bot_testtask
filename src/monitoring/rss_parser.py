import feedparser


def parser_news(
        data_dict: dict[str, str]
) -> list[dict[str, list[dict[str, str, str]]]]:
    """
    Преобразует данные полученные из RSS в словарь.
    :return: [{'name': url, 'news': [{link, pubdate, title}, ...]}, ...]
    """
    news = []

    for url, content in data_dict.items():
        titles = []
        content = feedparser.parse(content)

        for item in content.entries:
            titles.append(
                {
                    'link': item.link,
                    'pubdate': item.published,
                    'title': item.title
                }
            )
        news.append({'name': url, 'news': [*titles]})
    return news
