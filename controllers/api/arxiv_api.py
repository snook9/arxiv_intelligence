import urllib, urllib.request
from .api_interface import ApiInterface

class ArxivApi(ApiInterface):
    def getData(self):
        url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
        data = urllib.request.urlopen(url)
        return data
