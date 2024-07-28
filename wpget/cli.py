#!/usr/bin/env python
import json
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import urlparse
from wpget import get_posts


def main():
  parser = ArgumentParser(
    "wpget",
    description="Download all posts from a WordPress website via public JSON API.",
  )

  parser.add_argument(
    "-u", "--url", type=str, required=True, help="Base URL of the website."
  )
  parser.add_argument(
    "-o", "--output", type=Path, required=False, help="Output JSON file"
  )
  parser.add_argument(
    "-w",
    "--overwrite",
    action="store_true",
    default=False,
    help="Overwrite existing output file.",
  )

  parser.add_argument(
    "-j", "--nproc", type=int, required=False, default=None, help="Number of Processes"
  )

  parser.add_argument(
    "-r", "--retry", type=int, required=False, default=10, help="Max retries"
  )
  
  parser.add_argument(
    "-p", "--per_page", type=int, required=False, default=100, help="Per page"
  )

  args = parser.parse_args()

  output_file = None
  if args.output is not None:
    args.output.parent.mkdir(exist_ok=True)
    output_file = str(args.output)

  base_url = args.url.lower()

  if not base_url.startswith("https://") and not base_url.startswith("http://"):
    base_url = "http://" + base_url

  hostname = urlparse(base_url).hostname

  if output_file is None:
    output_file = f"{hostname}-data.jsonl"

  if not args.overwrite and Path(output_file).exists():
    print(f"Output file ({output_file}) already exists!")
    exit(-1)

  posts_iterator = get_posts(base_url, nproc=args.nproc, max_retries=args.retry, per_page=args.per_page)
  with open(output_file, "w") as outfile:
    for posts in posts_iterator:
      for post in posts:
        json_str = json.dumps(post, ensure_ascii=False)
        outfile.write(json_str + "\n")


if __name__ == "__main__":
  main()
