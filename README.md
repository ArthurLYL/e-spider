# E-spider

## Environment

IDE: PyCharm

Python: 3.7.4

requests: 2.23.0

os

BeautifulSoup4: 4.9.1

## About running

`download.py`: Download comic using given gallery URL (eg. https://e-hentai.org/g/xxxxxx/xxxxxx/). This file is just a  reference code from others and it will not be updated it in the future. 

`spider.py`: It can search comics according to user's will, and it will download all searched comics. Basing on low coupling, download function (aiming at search results, gallery or only one page) can be used according to user's need.

## TODO list

1. ~~Catch exception~~
2. ~~Request timeout processing(timeout threshold and maximum number of re-requests)~~
3. Augmenting robustness
4. Using IPProxyPool to cope with IP detection (I randomly set period to limit request interval for now)
5. Using Redis to re-download files that filed to download in `dir_url`.
6. Better user experience (maybe console interation), better modular code.

