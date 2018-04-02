import requests
from lxml import etree


class MySpider:
    def getWebContent(self, url, method, body={}):
        """
        get the html content from the url
        :param url:
        :param method: get or post
        :return:
        """
        if method == 'get':
            r = requests.get(url)
        else:
            r = requests.post(url, body)
        return r.text  # text is str, but content is byte str

    def getInfoInXPath(self, html, pattern):
        """
        get info in that XPATH: //*[@id="rso"]/div[1]/div/div[1]/div/div/h3/a

        :param pattern: string(//*[@id="eow-title"]/text())
        :return: content of a tag
        """
        text = etree.HTML(html)
        ele = text.xpath(pattern)
        return ele

