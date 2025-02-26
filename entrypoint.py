#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from random import choice
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from datetime import datetime
from atoma import parse_rss_bytes
from utils import u, html_unescape, filter_json_index_by_year

json_index_content = {}

# Azcodez
facebook_page_id = os.environ.get('FACEBOOK_PAGE_ID')
facebook_access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
facebook_api_end = 'https://graph.facebook.com/{0}/feed'.format(facebook_page_id)
facebook_api_photo_end = 'https://graph.facebook.com/{0}/photos'.format(facebook_page_id)

# MYM
facebook_page_id_mym = os.environ.get('FACEBOOK_PAGE_ID_MYM')
facebook_access_token_mym = os.environ.get('FACEBOOK_ACCESS_TOKEN_MYM')
facebook_api_end_mym = 'https://graph.facebook.com/{0}/feed'.format(facebook_page_id_mym)

# MotivateNotes
facebook_page_id_motivateNotes = os.environ.get('FACEBOOK_PAGE_ID_MOTIVATENOTES')
facebook_access_token_motivateNotes = os.environ.get('FACEBOOK_ACCESS_TOKEN_MOTIVATENOTES')
facebook_api_photo_end_motivateNotes = 'https://graph.facebook.com/{0}/photos'.format(facebook_page_id_motivateNotes)

# Feed url - Hashcode
feed_url = os.environ.get('FEED_URL')
feed_data = parse_rss_bytes(urlopen(feed_url).read())

# If in below timeslot post
current_timestamp = int(datetime.now().strftime('%Y%m%d%H%M%S'))
current_hour = int(datetime.now().strftime('%H'))
# if current_hour not in [9, 13, 15, 22]:
#     print('Script wasnt called in a recommended hour. Aborting.')
#     sys.exit(0) 

# Shuffle though xml link
for post in feed_data.items:
    post_timestamp = post.pub_date.strftime('%Y%m%d%H%M%S')
    json_index_content[post_timestamp] = {
        'title': post.title,
        'url': post.guid,
        'date': post.pub_date
    }

json_index_filtered = filter_json_index_by_year(json_index_content)

if not json_index_filtered:
    print('There are no posts to publish. Aborting.')
    sys.exit(0)

random_post_id = choice(list(json_index_filtered.keys()))
random_post_title = json_index_filtered[random_post_id]['title']
random_post_title = u(html_unescape(random_post_title))
random_post_url = u('{0}#{1}'.format(
    json_index_filtered[random_post_id]['url'],
    current_timestamp))

# Azcodez
facebook_api_data = {'message': random_post_title,
                     'link': random_post_url,
                     'access_token': facebook_access_token}
http_request = Request(url=facebook_api_end, method='POST',
                       data=urlencode(facebook_api_data).encode())
# facebook_api_data_two = {'message': 'Testing',
#                      'link': random_post_url,
#                      'access_token': facebook_access_token}
# http_request_two = Request(url=facebook_api_end, method='POST',
#                        data=urlencode(facebook_api_data_two).encode()) 

# MYM post
facebook_api_data_mym = {'message': 'Motivation',
                        'link': 'https://youtu.be/tnWR1wMxFWs',
                        'access_token': facebook_access_token_mym}
http_request_mym = Request(url=facebook_api_end_mym, method='POST', data=urlencode(facebook_api_data_mym).encode())

# AzCodez Photo post
# facebook_api_data_photo = {'url': 'https://azcodez.com/images/150633b813614aa8b24cd8459fcf0b21.png',
#                      'access_token': facebook_access_token}
# http_request_photo = Request(url=facebook_api_photo_end, method='POST',
#                        data=urlencode(facebook_api_data_photo).encode())

# Motivate Notes Photo post
# facebook_api_data_photo_motivateNotes = {'url': 'https://azcodez.com/images/150633b813614aa8b24cd8459fcf0b21.png',
#                                          'access_token': facebook_access_token_motivateNotes}
# http_request_photo_motivateNotes = Request(url=facebook_api_photo_end_motivateNotes, method='POST',
#                                            data=urlencode(facebook_api_data_photo_motivateNotes).encode())
facebook_api_data = {'message': random_post_title,
                     'link': random_post_url,
                     'access_token': facebook_access_token}
http_request = Request(url=facebook_api_end, method='POST',
                       data=urlencode(facebook_api_data).encode())

# Chairmans post
# Get few urls and shuffle them and post

# TIH

# Azcodes post
count = 0
while count < 1:
    try:
        result = json.loads(str(urlopen(http_request).read(), 'utf-8'))
        #time.sleep(3)
    except Exception as e:
        print('There was an error publishing: {0}'.format(e))
        count += 1
        continue
    if 'error' in result:
        count += 1
        continue
    print('Successfully published!: {0}'.format(random_post_url))
    break

# MYM post
# count = 0
# while count < 1:
#     try:
#         # time.sleep(60)
#         result = json.loads(str(urlopen(http_request_mym).read(), 'utf-8'))
#     except Exception as e:
#         print('There was an error publishing: {0}'.format(e))
#         count += 1
#         continue
#     if 'error' in result:
#         count += 1
#         continue
#     print('Successfully published!: {0}'.format(random_post_url))
#     break

# Motivate Notes Photo post
# count = 0
# while count < 1:
#     try:
#         # time.sleep(60)
#         result = json.loads(str(urlopen(http_request_photo_motivateNotes).read(), 'utf-8'))
#     except Exception as e:
#         print('There was an error publishing: {0}'.format(e))
#         count += 1
#         continue
#     if 'error' in result:
#         count += 1
#         continue
#     print('Successfully published photo!: ')
#     break