#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Web Scraper
"""
__author__ = "Your Github Username"

import argparse
import requests
import re
from MyHTMLParser import MyHTMLParser
from pprint import pprint

parser = MyHTMLParser()


def request_url(url):
    r = requests.get(url)
    html_text = r.content

    url_list = list(set(re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_text)))

    email_list = list(
        set(re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', html_text)))

    parser.feed(html_text)
    phone_list = []
    for d in parser.data:
        phone_regex = r'\W*\D([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?\D'
        matches = re.search(phone_regex, d)
        if matches:
            phone_list.append(
                '({}){}-{}'.format(matches.group(1), matches.group(2), matches.group(3)))

    print('URLs')
    pprint(url_list)
    print('email addresses')
    pprint(email_list)
    print('Phone Numbers')
    pprint(phone_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Input URL to be scraped')

    args = parser.parse_args()
    if args.url:
        request_url(args.url)


if __name__ == "__main__":
    main()
