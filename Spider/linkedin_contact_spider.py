from Security.spider.spider import MySpider

"""
    capture info in LinkedIn within my track, auto connect, gather corporation of those people and url from "experience"
    Modules using:
        requests: get/post request
        lxml: xpath
"""

MAXPAGE = 100

def getAllContact(spy):
    # get all contact through search in LinkedIn
    # https://www.linkedin.com/search/results/index/?keywords=software%20engineer&origin=GLOBAL_SEARCH_HEADER
    keywords = ["Software Engineer", "Software Developer", "Information Analysis", "Security Manager"]
    patterns = {
        "url": "",
        "Name": ""
    }
    resSet = {

    }
    for keyword in keywords:
        keyword.replace(' ', '%20')
        for page in range(MAXPAGE):
            url = "https://www.linkedin.com/search/results/index/?keywords=%s&origin=GLOBAL_SEARCH_HEADER&page=%s" % (keyword, page)
            text = spy.getWebContent(url).text
            spy.getInfoInXPath(text, pattern="")

def autoConnect():
    # analyze the connect process by Burpsuite
    return

def writeInFile():
    # Corp is write into SDEinfo.html, For me to apply
    with open("SDEinfo.html", 'w') as sdeInfo:
        sdeInfo.write("<!DOCTYPE html><html><head><title>Just Apply!</title></head><body>")
        for corpName, corpUrl in getCorpUrl():
            sdeInfo.write("<a href = '%s'> %s </a>\n" % (corpUrl, corpName))
        sdeInfo.write("</body></html>")

def getCorpUrl():
    return


def main():
    spy = MySpider()
    getAllContact(spy)

if __name__ == '__main__':
    main()