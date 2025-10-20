import os, requests, time
from googleapiclient.discovery import build
from tqdm import tqdm

def google_image_search(api_key, cx, query, num=20, start=1):
    """Return list of image URLs using Google Custom Search JSON API."""
    service = build("customsearch", "v1", developerKey=api_key)
    urls = []
    # Google CSE returns up to 10 results per request
    while len(urls) < num:
        resp = service.cse().list(q=query, cx=cx, searchType='image',
                                  start=start, num=min(10, num - len(urls))).execute()
        items = resp.get('items', [])
        for it in items:
            link = it.get('link')
            if link:
                urls.append(link)
        start += len(items)
        if not items:
            break
        time.sleep(1)
    return urls

def download_images(urls, save_dir, prefix="img", timeout=8):
    os.makedirs(save_dir, exist_ok=True)
    saved = []
    for i, url in enumerate(tqdm(urls), 1):
        try:
            r = requests.get(url, timeout=timeout, stream=True)
            r.raise_for_status()
            ext = url.split('.')[-1].split('?')[0]
            if ext.lower() not in ['jpg','jpeg','png','gif','webp','bmp']:
                ext = 'jpg'
            fname = f"{prefix}_{i:03d}.{ext}"
            path = os.path.join(save_dir, fname)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            saved.append({'filename': fname, 'url': url, 'path': path})
        except Exception:
            # skip bad url
            continue
    return saved
