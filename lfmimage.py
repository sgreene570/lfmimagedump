"""
Last.fm image dump script.
Uses the Last.fm api to fetch album arts for user's top 50 albums.
@author: sgreene570
"""


import requests
from tqdm import tqdm
import json
import argparse
import urllib.request
import os


LFMAPI_URL = "http://ws.audioscrobbler.com/2.0/"
ALBUM_ART_DIRECTORY = "albumart"
# Order in which s/m/l images appear in the json object from the lfm api
SMALL_ART_INDEX = 1
MEDIUM_ART_INDEX = 2
LARGE_ART_INDEX = 3
DEFAULT_SIZE_INDEX = MEDIUM_ART_INDEX


def get_top_album_art(username, size_index):
    top_albums = requests.get(LFMAPI_URL + "?method=user.gettopalbums&user="
                            + username + "&api_key=" + LFMAPI_KEY
                            + "&format=json").json()
    if "error" in top_albums.keys():
        print("Error: Check Username?")
        os._exit(1)

    for album in tqdm(top_albums["topalbums"]["album"]):
        url = album["image"][size_index]["#text"].rstrip()
        if url is not '':
            if not os.path.exists(ALBUM_ART_DIRECTORY):
                os.makedirs(ALBUM_ART_DIRECTORY)

            filename = os.path.join(ALBUM_ART_DIRECTORY, album["name"] + ".png")
            urllib.request.urlretrieve(url, filename)


def main():
    parser = argparse.ArgumentParser(description="Last.fm image dump")
    parser.add_argument("username", type=str, nargs=1, help="Last.fm username")
    parser.add_argument("--small", action="store_true", help="Fetch smaller images")
    parser.add_argument("--large", action="store_true", help="Fetch larger images")
    args = parser.parse_args()
    size_index = DEFAULT_SIZE_INDEX
    if args.small:
        size_index = SMALL_ART_INDEX
    elif args.large:
        size_index = LARGE_ART_INDEX

    get_top_album_art(str(args.username).strip("[']"), size_index)


if __name__ == "__main__":
    main()
