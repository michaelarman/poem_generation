import os
import requests
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def get_links(link):
    '''
    This function gathers all the links of the poem website which is used for the subsequent
    scrape function. Basically this retrieves all links for the independent poems. On this
    particular poems website, there are two main categories to obtain poems. The first is categorized by poem
    forms (e.g. haiku, sonnet, etc.) and the other category being topic.

    :param link: str link of either poem topics or poem forms
    :return: array of links for scraping
    '''
    r = requests.get(link) # start with accessing poem topics
    raw_html = r.content
    soup = BeautifulSoup(raw_html, 'html.parser')

    ul = soup.find("ul", {"class": "subjectsMain-list"}) 
    links = [a.get('href') for a in ul.find_all('a', href=True)] # get all links of the poem topics

    poem_links = []
    for l in links: # for each href get the full link
        poem_links.append(base_url+l) 

    return poem_links

def create_directories(links, top=True):
    '''
    This is to create the directories for storing the poem txt files.
    The structure is as follows:
    Data
        Forms
            Type of Form
            Type of Form
            .
            .
            .
                        poems
        Topics
            Type of Topic
            Type of Topic
            .
            .
            .
                        poems

    :param links: array, The poem links obtained from the get_links() function
    :param top: bool, flag for whether you are creating the directories for the topic or forms categories
    '''
    topics_forms = [t.split("/")[-2] for t in links]
    for t in topics_forms:
        if top:
            os.makedirs(os.path.join('data/', 'topics', t))
        else:
            os.makedirs(os.path.join('data/', 'forms', t))


def scrape(links, top=True):

    '''
    This is where all the scraping happens. It loops through the poem links and collects the text from each one.
    It
    :param links: array, The poem links obtained from the get_links() function
    :param top: bool, flag for whether you are creating the directories for the topic or forms categories
    :return:
    '''
    for i,topic in enumerate(links):
        r = requests.get(topic)
        next_page = requests.get(topic + '/page-2/') # there can be multiple pages for each topic or form
        raw_html = r.content
        next_html = next_page.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        soup_next = BeautifulSoup(next_html, 'html.parser')
        poem_list = soup.find("ol", {"class": "rpoems-list"})
        next_poem_list = soup_next.find("ol", {"class": "rpoems-list"})
        poem_pages = []
        next_pages = []
        topics = [t.split("/")[-2] for t in links]
        try:
            for l in poem_list.find_all('li'):
                poem_pages.append(base_url + l.get('onclick').split("'")[1]) # append each inidividual page of poems
        except:
            pass
        try:
                for p in poem_pages:
                    r = requests.get(p, verify=False) # bad practice to make verify False but I was getting some errors
                    raw_html = r.content
                    soup = BeautifulSoup(raw_html, 'html.parser') 
                    title = soup.title.text.strip()
                    poem = soup.find('p', {"style": "display:block; width:330px; float:left;"})
                    poem = [text for text in poem.stripped_strings]
                    poem = '\n'.join(str(p) for p in poem)
                    if top:
                        with open('./{}.txt'.format(os.path.join('data/topics', topics[i], ''.join(e for e in title if e.isalnum()))),
                        mode='wt', encoding='utf-8') as file:
                            file.write(poem)
                    else:
                        with open('./{}.txt'.format(os.path.join('data/forms', topics[i], ''.join(e for e in title if e.isalnum()))),
                        mode='wt', encoding='utf-8') as file:
                            file.write(poem)
        except:
            pass
        # scrape the next page
        try:
            for l in next_poem_list.find_all('li'):
                next_pages.append(base_url + l.get('onclick').split("'")[1])
        except:
            pass
        try:
                for p in next_pages:
                        r = requests.get(p, verify=False)
                        raw_html = r.content
                        soup = BeautifulSoup(raw_html, 'html.parser') 
                        title = soup.title.text.strip()
                        poem = soup.find('p', {"style": "display:block; width:330px; float:left;"})
                        poem = [text for text in poem.stripped_strings]
                        poem = '\n'.join(str(p) for p in poem)
                        if top:
                            with open('./{}.txt'.format(os.path.join('data/topics', topics[i], ''.join(e for e in title if e.isalnum()))),
                            mode='wt', encoding='utf-8') as file:
                                file.write(poem)
                        else:
                            with open('./{}.txt'.format(os.path.join('data/forms', topics[i], ''.join(e for e in title if e.isalnum()))),
                            mode='wt', encoding='utf-8') as file:
                                file.write(poem)
        except:
            pass
            

if __name__ == '__main__':
    base_url = 'https://www.poemhunter.com' #home page
    poem_topics = 'https://www.poemhunter.com/poem-topics/' #topics page
    poem_forms = 'https://www.poemhunter.com/poem-forms/' # poem types page


    poem_links = get_links(poem_topics)
    # create directories to store the poems
    create_directories(poem_links)
    print('Directories Created.')
    print('Scraping topics...')
    scrape(poem_links)

    poem_links = get_links(poem_forms)
    # create directories to store the poems
    create_directories(poem_links,top=False)
    print('Directories Created.')
    print('Scraping forms...')
    scrape(poem_links,top=False)

