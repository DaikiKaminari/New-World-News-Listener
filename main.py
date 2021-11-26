import requests
import json
from win10toast import ToastNotifier

notifier_ = ToastNotifier()


def get_latest_articles(latest_id, api_uri):
    r = requests.get(api_uri)
    new_lastest_id = latest_id
    new_articles = []
    if r.status_code != 200:
        print("Error : request returned the status code " + str(r.status_code))
        return
    for article in r.json():
        if article["language"] is not None:
            continue
        if article["id"] < latest_id:
            continue
        new_lastest_id = article["id"]
        new_articles.append(article)
    return new_lastest_id, new_articles


def notif(notifier, title, message):
    notifier.show_toast(
        title=title,
        msg=message,
        duration=100000,
        icon_path="resources/NW_Icon1.ico",
        threaded=True
    )


def main():
    while True:
        with open('info.json', 'r') as f:
            info = json.load(f)
        info["latest_id"], latest_articles = get_latest_articles(info["latest_id"], info["api_uri"])
        with open('info.json', 'w') as f:
            f.write(json.dumps(info))
        for new_article in latest_articles:
            notif(notifier_, new_article["title"], new_article["source_url"])


main()
# notif(notifier_, "title_test", "message_test")
