import os
import re
import requests
from os.path import basename
from bs4 import BeautifulSoup

def get_links(link):

    r = requests.get(link) # start with accessing poem topics
    raw_html = r.content
    soup = BeautifulSoup(raw_html, 'html.parser')

    ul = soup.find("ul", {"class": "subjectsMain-list"}) 
    links = [a.get('href') for a in ul.find_all('a', href=True)] # get all links of the poem topics

    poem_links = []
    for l in links: # for each href get the full link
        poem_links.append(base_url+l) 

    return poem_links

def create_directories(lst):

    topics_forms = [t.split("/")[-2] for t in lst]
    for t in topics_forms:
        os.mkdir(os.path.join('data/', t))

def scrape(lst):
    for i,topic in enumerate(lst):
        r = requests.get(topic)
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        poem_list = soup.find("ol", {"class": "rpoems-list"})
        poem_pages = []
        topics = [t.split("/")[-2] for t in poem_topics_links]
        for l in poem_list.find_all('li'):
            poem_pages.append(base_url + l.get('onclick').split("'")[1])
            for p in poem_pages:
                r = requests.get(p)
                raw_html = r.content
                soup = BeautifulSoup(raw_html, 'html.parser') 
                title = soup.title.text.strip()
                poem = soup.find('p', {"style": "display:block; width:330px; float:left;"})
                poem = [text for text in poem.stripped_strings]
                poem = '\n'.join(str(p) for p in poem)
                with open('./{}.txt'.format(os.path.join('data/', topics[i], ''.join(e for e in title if e.isalnum()))),
                mode='wt', encoding='utf-8') as file:
                    file.write(poem)

if __name__ == '__main__':
    base_url = 'https://www.poemhunter.com' #home page
    poem_topics = 'https://www.poemhunter.com/poem-topics/' #topics page
    poem_forms = 'https://www.poemhunter.com/poem-forms/' # poem types page


    poem_links = get_links(poem_topics)
    # create directories to store the poems
    
    create_directories(poem_links)
    print('Directories created.')
    scrape(poem_links)
    print('Scraping...')

