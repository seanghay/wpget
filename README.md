# wpget

A tool for downloading all posts from a WordPress website via public JSON API

```shell
pip install wpget

wpget -u "https://example.com" -j 8 -o data.jsonl
```

### Options

```
usage: wpget [-h] -u URL [-o OUTPUT] [-w] [-j NPROC] [-r RETRY] [-p PER_PAGE]

Download all posts from a WordPress website via public JSON API.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Base URL of the website.
  -o OUTPUT, --output OUTPUT
                        Output JSON file
  -w, --overwrite       Overwrite existing output file.
  -j NPROC, --nproc NPROC
                        Number of Processes
  -r RETRY, --retry RETRY
                        Max retries
  -p PER_PAGE, --per_page PER_PAGE
                        Per page
```