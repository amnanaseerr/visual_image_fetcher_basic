from PIL import Image
import os, imagehash
import pandas as pd

def resize_image(in_path, out_path, size=(224,224)):
    img = Image.open(in_path).convert('RGB')
    img = img.resize(size)
    img.save(out_path)

def filter_small_images(records, min_size=(50,50)):
    filtered = []
    for r in records:
        try:
            img = Image.open(r['path'])
            if img.size[0] < min_size[0] or img.size[1] < min_size[1]:
                continue
            filtered.append(r)
        except:
            continue
    return filtered

def deduplicate(records):
    seen = {}
    unique = []
    for r in records:
        try:
            h = str(imagehash.average_hash(Image.open(r['path'])))
            if h in seen:
                continue
            seen[h] = True
            unique.append(r)
        except:
            continue
    return unique

def save_metadata(records, save_csv):
    df = pd.DataFrame(records)
    df.to_csv(save_csv, index=False)


import requests
import pandas as pd

def download_images(url, path):
    try:
        img_data = requests.get(url, timeout=10).content
        with open(path, 'wb') as f:
            f.write(img_data)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def save_metadata(records, save_csv):
    df = pd.DataFrame(records)
    df.to_csv(save_csv, index=False)

