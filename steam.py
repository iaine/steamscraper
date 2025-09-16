'''
Steam Market Scraper
'''

from urllib.request import urlopen
import ssl 
import re
import pandas as pd

from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

class SteamScraper():
    
    def get_link_details(link):
        '''
        Get individual links and parse into structure
        :param link - the url
        :return list
        '''
        details = {}
        details['link'] = link
        appid = link.replace('https://store.steampowered.com/app/', '').split('/')[0]
        details['appid'] = appid
        data = urlopen(link, timeout=10)
        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        details['title'] = htmlParse.find("div", {'class': 'apphub_AppName'}).get_text()
        details['description'] = htmlParse.find("div", {'class': 'game_area_description'}).get_text()
        app_details = {}
        #find the genres
        genres = []
        for detail in htmlParse.find("div", {'id': 'genresAndManufacturer'}).find('span').find_all("a"):
            genres.append(detail.get_text())
        
        if len(genres) > 0: 
            details['genres'] = ";".join(genres)
        else: 
            details['genres'] = ""

        for detail in htmlParse.find("div", {'id': 'genresAndManufacturer'}).find_all('div'):
            devs = []
            pubs = []
            if detail.find('b').get_text().strip() == "Developer:":
                for dev in detail.find_all("a"): devs.append(dev.get_text())
                details['developers'] = ";".join(devs)
            elif detail.find('b').get_text().strip() == "Publisher:":
                for pub in detail.find_all("a"): pubs.append(pub.get_text())
                details['publisher'] = ";".join(pubs)

        return details

    def get_links_details(links):
        '''' Get the links of arrays '''
        link_details = []

        for l in links:
            link_details.append(get_link_details(l))
        
        return link_details

    def get_search(search_term, tag=""):
        '''
        Get links from the search page
        '''
        links = []
        if search_term == "": 
            raise ScraperException("Invalid Search Query. No search term entered.")

        base = f"https://store.steampowered.com/search/?term={search_term}"
        if tag != "": base += f"&tags={tag}"

        data = urlopen(base, timeout=10)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links

    def links_from_url(search_url):
        ''' Get the links '''
        data = urlopen(search_url, timeout=10)
        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        divs =  htmlParse.find('div', {'class':'similar_grid_ctn'})

        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links   


    def get_similar(app_id):
        '''Get Similar Apps'''
        links = []
        #simlink = "https://store.steampowered.com/recommended/morelike/app/2923300/?snr=1_5_9__300"
        
        simlink = f"https://store.steampowered.com/recommended/morelike/app/{app_id}/"
        data = urlopen(simlink, timeout=10)
        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        divs =  htmlParse.find('div', {'class':'similar_grid_ctn'})

        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links

    def get_developer(developer):
        '''Get Game Developer'''
        links = []
        devlink = f"https://store.steampowered.com/search/?developer={developer}"
        data = urlopen(devlink, timeout=10)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links

    def get_publisher(publish):
        '''Get Game publisher'''
        base = "https://store.steampowered.com/search/?publisher={}".format(publish)
        links = []
        data = urlopen(base, timeout=10)
        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links    


    def get_tags(tag):
        links = []
        devlink = f"https://store.steampowered.com/tags/en/{tag}/"
        data = urlopen(devlink, timeout=10)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if ah.startswith("https://store.steampowered.com/app"):
                links.append(para.get('href'))
        return links

    def write_csv(linksarray, fname):
        '''
        Write the links to a file
        '''
        df = pd.DataFrame(linksarray)
        df.to_file(fname, index=False)

    def reviews(appid):
        """
        Get reviews
        """
        base = "https://steamcommunity.com/app/1030300/reviews"
