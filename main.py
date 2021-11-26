import requests
import json
import webbrowser
import time
from win10toast_click_custom import ToastNotifier


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


def open_browser(page_url):
    try:
        webbrowser.open(page_url, new=2, autoraise=False)
    except:
        print('Failed to open URL. Unsupported variable type.')


def notif(title, message):
    notifier = ToastNotifier()
    notifier.show_toast(
        title=title,
        msg=message,
        duration=None,
        icon_path="resources/NW_Icon1.ico",
        threaded=True
    )


def main():
    interupted = False
    while not(interupted):
        with open('info.json', 'r') as f:
            info = json.load(f)
        new_lastest_id, latest_articles = get_latest_articles(info["latest_id"], info["api_uri"])
        with open('info.json', 'w') as f:
            info["latest_id"] = new_lastest_id
            f.write(json.dumps(info))
        for new_article in latest_articles:
            notif(new_article["title"], new_article["source_url"])
            open_browser(new_article["source_url"])
        time.sleep(10)


main()
