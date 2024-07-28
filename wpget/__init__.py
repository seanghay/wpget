import multiprocessing as mp
from collections import OrderedDict
from urllib.parse import urlencode, urljoin

import urllib3
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


def get_page(args):
  url, max_retries = args
  retries = Retry(total=max_retries, backoff_factor=0.1)
  session = Session()
  session.mount("https://", HTTPAdapter(max_retries=retries))
  res = session.get(url, allow_redirects=True, verify=False)
  return res.json()


def get_page_count(url):
  session = Session()
  res = session.head(url, allow_redirects=True, verify=False)

  if res.status_code != 200:
    return None

  total_pages = int(res.headers["x-wp-totalpages"])
  total_posts = int(res.headers["x-wp-total"])
  return total_pages, total_posts


def get_posts(base_url, nproc=None, max_retries=10):
  url = urljoin(base_url, "/wp-json/wp/v2/posts")
  page_count_result = get_page_count(url)

  if page_count_result is None:
    raise Exception("Not a WordPress website. Unable to get the total pages.")

  total_pages, total_posts = page_count_result

  paged_urls = [
    (url + "?" + urlencode(OrderedDict(page=page_idx + 1)), max_retries)
    for page_idx in range(total_pages)
  ]

  print(f"Found {total_posts:,} posts")
  with tqdm(total=total_pages, desc=base_url, ascii=True) as pbar:
    with mp.Pool(nproc) as pool:
      for posts in pool.imap_unordered(get_page, paged_urls):
        yield posts
        pbar.update()