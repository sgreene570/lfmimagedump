"""
Last fm image dump script.
@author: Stephen Greene
"""


import requests
import json
import argparse
import urllib.request
import os


LFMAPI_URL = "http://ws.audioscrobbler.com/2.0/"
LFMAPI_KEY = "0442ba22ce10eb034c902991cd0d2685"
ALBUM_ART_DIRECTORY = "albumart"


def get_top_album_art(username):
    top_albums = requests.get(LFMAPI_URL + "?method=user.gettopalbums&user="
                            + username + "&api_key=" + LFMAPI_KEY
                            + "&format=json").json()

    for album in top_albums["topalbums"]["album"]:
        url = album["image"][2]["#text"].rstrip()
        if url is not '':
            if not os.path.exists("albumart"):
                os.makedirs(ALBUM_ART_DIRECTORY)

            filename = os.path.join(ALBUM_ART_DIRECTORY, album["name"] + ".png")
            urllib.request.urlretrieve(url, filename)


def main():
    parser = argparse.ArgumentParser(description="last fm image dump")
    parser.add_argument("username", type=str, nargs=1, help="Last.fm username")
    args = parser.parse_args()
    get_top_album_art(str(args.username).strip("[']"))


if __name__ == "__main__":
    main()
