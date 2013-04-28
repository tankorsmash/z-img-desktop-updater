"""
Written for Python 2.7 on Windows 7x64


Some other searches, as featured in several subreddit sidebars are located in a
text file called searches.txt, which is just a list a names from subreddits like
/r/gentlemanboners

"""

import ctypes, random
#both of these are on pip, I'm sure
import requests, bs4
import ipdb


SEARCHES_TXT = r"searches.txt"

#search for image
def search_image(query):

    image_path = download_image(query)

    return image_path


#download image
def download_image(query):

    parsed_query = query.strip().replace(" ", '+')
    # url = r"https://www.google.com/search?safe=off&hl=en&site=imghp&tbs=isz:l&tbm=isch&sa=1&q={query}".format(query=parsed_query)
    url = r"http://z-img.com/search.php?&ssg=off&size=large&q={query}".format(query=parsed_query)
    r = requests.get(url)
    html = r.text

    image_url = parse_for_image_url(html)
    image_path = save_image(image_url)

    return image_path


#parse for image
def parse_for_image_url(html):

    #fix for python crashing, fixed in 2.4.5 lxml, I'm pretty sure
    html = html.replace(r"<!DOCTYPE>", "")

    soup = bs4.BeautifulSoup(html)
    res = soup.findAll("img")

    good_links = []

    #remove bad links
    for img in res:
        if img['src'] == r'imgs/direct.jpg':
            # ignore 'badlink'
            pass
        else:
            # print img['src']
            good_links.append(img['src'])

    #select a random image
    image_url = random.choice(good_links)

    return image_url


def save_image(image_url):
    image_path = r'c:/scarjo.jpg'

    with open(image_path, 'wb') as f:
        r = requests.get(image_url)
        f.write(r.content)
        print "done writing to", image_path

    return image_path


#set as wallpapper
def set_wallpaper(image_path):

    SPI_SETDESKWALLPAPER = 20
    sucessful = ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER,
                                               0, image_path, 0)

    if not sucessful:
        print "Use recursion to choose another image at random"
        use_random_image()


def query_to_wallpaper(query):
    image_path = search_image(query)
    set_wallpaper(image_path)

    return image_path


#choose a random name from the list and set that as wallpaper
def query_from_list():

    with open(SEARCHES_TXT) as f:
        queries = f.readlines()
        query = random.choice(queries)

    return query


def use_random_image():
    query = query_from_list()
    query_to_wallpaper(query + " hot")


def main(query):

    query = query_from_list()

    query_to_wallpaper(query + " hot")




if __name__ == "__main__":

    main("scarlett johansson")

