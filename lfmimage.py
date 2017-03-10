"""
Last fm image dump script.
@author: Stephen Greene
"""


import requests
import json
import argparse
import urllib.request


LFMAPI_URL = "http://ws.audioscrobbler.com/2.0/"


def main():
    parser = argparse.ArgumentParser(description="last fm image dump")
    parser.add_argument("username", type=str, nargs=1, help="Last.fm username")
    args = parser.parse_args()
    top_albums = requests.get(LFMAPI_URL + "?method=user.gettopalbums&user="
                    + str(args.username).strip("[']") + "&api_key="
                    + LFMAPI_KEY + "&format=json").json()

    for album in top_albums["topalbums"]["album"]:
        url = album["image"][2]["#text"].rstrip()
        if url is not '':
            urllib.request.urlretrieve(url, (album["name"] + ".png"))


if __name__ == "__main__":
    main()
