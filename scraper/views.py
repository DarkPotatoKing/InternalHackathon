# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

import urllib2
import json

# Create your views here.
def index(request):
    return HttpResponse('<br>'.join(search_links_in_google(['duterte', 'fake', 'news', 'law'])))

def test(name = 'potato'):
    return HttpResponse("Hello, {}. You're at the scraper index.".format(name))

# Searches google using the keywords stored as a list of strings as query.
# Returns a list of strings containing urls to the news site.
# Some url domains [YouTube, Wikipedia] links are filtered out
def search_links_in_google(keywords = ['This', 'is', 'a', 'sample', 'query']):
    # list of urls to exclude from list of urls
    exclude_url = ['youtube.com', 'en.wikipedia.org']

    api_key = 'AIzaSyB-5OXK0gKW50L-gJRt5vWlKz2-WAGY-lI'
    custom_search_id = '014135143817107886589:97tdpkyrjl0'

    # Query by issuing a GET request to google search api
    url = 'https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}'.format(api_key, custom_search_id, '+'.join(keywords))
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    content = urllib2.urlopen(request)
    response = content.read()

    # parse json response
    parsed = json.loads(response)

    # get list of links
    unfiltered_links = [i['link'] for i in parsed['items']]

    # filter out links
    filtered_links = []
    for link in unfiltered_links:
        is_excluded = False
        for e in exclude_url:
            if link.find(e) != -1:
                is_excluded = True
                break

        if not is_excluded:
            filtered_links.append(link)

    return filtered_links
