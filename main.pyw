import requests
import json
import webbrowser
import time
from PIL import Image
import pystray
from multiprocessing import Process, Manager
from win10toast_click_custom import ToastNotifier


# UTILS#
def open_browser(page_url):
    try:
        webbrowser.open(page_url, new=2, autoraise=False)
    except:
        print("Failed to open URL. Unsupported variable type.")


def open_links(links):
    for link in links:
        open_browser(link)


def notify(title, message):
    notifier = ToastNotifier()
    notifier.show_toast(
        title=title,
        msg=message,
        duration=None,
        icon_path="resources/NW_Icon1.ico",
        threaded=True
    )


# FUNCTIONS #
# create a system stray icon that can :
# - open latest NW news links
# - kill the program
def create_system_stray_icon(links):
    icon = pystray.Icon("NW News Listener")
    icon.title = "NW News Listener"
    with Image.open("resources/NW_Icon1.ico") as ico:
        icon.icon = ico

    menu_item1 = pystray.MenuItem("Ouvrir les liens", lambda: open_links(links))
    menu_item2 = pystray.MenuItem("Quitter", icon.stop)
    menu = pystray.Menu(menu_item1, menu_item2)
    icon.menu = menu
    icon.run()


# returns a couple composed of the latest news id and the last news
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
        new_lastest_id = max(new_lastest_id, article["id"])
        new_articles.append(article)
    return new_lastest_id, new_articles


# check every minute if there is news published in english, if so then send a Windows notification and open links
def listen_and_notify(links):
    while True:
        with open("info.json", "r") as f:
            info = json.load(f)
        new_latest_id, latest_articles = get_latest_articles(info["latest_id"], info["api_uri"])
        with open("info.json", "w") as f:
            info["latest_id"] = new_latest_id+1
            f.write(json.dumps(info))
        for new_article in latest_articles:
            links.append(new_article["source_url"])
            # notify(new_article["title"], new_article["source_url"])
            # open_browser(new_article["source_url"])
        time.sleep(60)


# MAIN #
def main():
    if __name__ == "__main__":
        links = Manager().list()
        p1 = Process(target=create_system_stray_icon, args=(links,))
        p1.start()
        p2 = Process(target=listen_and_notify, args=(links,))
        time.sleep(1)
        p2.start()
        p1.join()
        p2.kill()


main()
