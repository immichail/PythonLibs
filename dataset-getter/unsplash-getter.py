from bs4 import BeautifulSoup as bs
import requests
import json
import io
from PIL import Image
import os


url = "https://api.unsplash.com/search/photos"
ACCESS_TOKEN = "e5b520fc636a81268c0efd733f3cbf84d64565df7233c53e27cba3e25b35ba6f"
imgs_folder = "./data/"

def get(query = "", page = 1):
    print("Sending request for query " + query + " page = " + str(page))
    params = {
        "client_id": ACCESS_TOKEN,
        "query": query,
        "page": page,
        "per_page": 100
    }
    r = requests.get(url, params = params)
    body = json.loads(r.content)

    imgs = {img['id'] : img['urls']['regular'] for img in body['results']}

    return imgs

def get_n_images(n, query = ""):
    imgs = {}
    page = 1

    while (len(imgs) < n):

        imgs.update(get(query = query, page = page))

        page += 1

    return imgs

def get_img_url(url):
    img = None
    r = requests.get(url)
    img = Image.open(io.BytesIO(r.content))
    return img

def save_img(name, img):
    img.save(imgs_folder + name + ".jpg", "JPEG")
    print("image " + name + " saved")
    return

def get_index(filepath = "../dataset-mapper/box.csv"):
    ids = []
    with open(filepath, 'r') as f:
        for line in f:
            ids.append(line.split(',')[0].replace('.jpg', ''))
    
    return ids

def append_dir_to_index(filepath):
    index = []
    filenames = os.listdir(filepath)
    for name in filenames:
        index.append(name.replace('.jpg', ''))

    return index

if __name__ == "__main__":

    ids = get_index()
    ids.append(append_dir_to_index('./data'))

    imgs = get_n_images(2000, query = "food")

    for id, url in imgs.items():
        if not( id in ids):
            try:
                save_img(id, get_img_url(url))
            except:
                print("Unable to save img ", id)