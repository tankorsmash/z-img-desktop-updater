"""
Written for Python 2.7 on Windows 7x64


Some other searches, as featured in several subreddit sidebars are located in a
text file called searches.txt, which is just a list a names from subreddits like
/r/gentlemanboners

"""


import ctypes, random, re

#both of these are on pip, I'm sure
import requests, bs4


SEARCHES_TXT = r"searches.txt"
IMAGE_PATH = r"c:/scarjo.jpg"

#search for image
def search_image(query, engine):
    """
    Calls download_image... should remove this
    """

    image_path = download_image(query, engine)

    return image_path


#download image
def download_image(query, engine='zimg'):
    """
    Downloads an image as described by the query and taken from the search engine
    'engine'. Can be 'zimg' for z-img.com (Google) or 'bing' for Bing.com
    """

    parsed_query = query.strip().replace(" ", '+')

    if engine == 'zimg':
        image_url = parse_zimg_for_image_url(query)
    elif engine == 'bing':
        image_url = parse_bing_for_image_url(query)
    image_path = save_image(image_url)

    return image_path


#parse for image
def parse_zimg_for_image_url(query):
    """
    Pulls all the image links from a Z-Img.com page, which is just a nice wrapper
    for the Google Image Search
    """
    print 'using zimg'
    # url = r"https://www.google.com/search?safe=off&hl=en&site=imghp&tbs=isz:l&tbm=isch&sa=1&q={query}".format(query=parsed_query)
    url = r"http://z-img.com/search.php?&ssg=off&size=large&q={query}".format(query=query)
    r = requests.get(url)
    html = r.text

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


def parse_bing_for_image_url(query):
    """
    Pulls all the image links from a Bing Image Search
    """
    print 'using bing'
    url = r'http://www.bing.com/images/search?q={query}&qft=%2Bfilterui%3Aimagesize-large'.format(query=query)

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content)
    res = soup.findAll('div', {'class': 'dg_u'})

    good_links = []

    # find the 'a' elem, then the 'm' attr. Then split the string on 'oi:'
    # and pull the messy html out. Then using regex, pull out the URL and
    # save that to a list
    for div in res:
        a_elem = div.find('a')
        m_attr = a_elem.get('m')
        if m_attr:
            dirty_url = m_attr.split('oi:')[-1]
            pattern = "http:.*.jpg"
            matches = re.findall(pattern, dirty_url)
            if matches:
                cleaned_url = matches[0]
                good_links.append(cleaned_url)

    image_url = random.choice(good_links)
    return image_url


def save_image(image_url):
    """
    Saves the given image_url and returns the local file path that it was
    saved to.
    """
    image_path = IMAGE_PATH

    with open(image_path, 'wb') as f:
        headers = {'user-agent': "z-img-desktop-updater"}
        r = requests.get(image_url, headers=headers)
        f.write(r.content)
        print "done writing to IMAGE_PATH:", image_path

    return image_path


#set as wallpapper
def set_wallpaper(image_path, engine='zimg'):
    """
    Sets the Windows Wallpaper to the image located at image_path
    """

    SPI_SETDESKWALLPAPER = 20
    sucessful = ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 0)

    if not sucessful:
        print "Use recursion to choose another image at random"
        use_random_image(engine)


def query_to_wallpaper(query, engine='zimg'):
    """
    take a string query, downloads an image from the given search engine,
    then changes the Windows Wallpaper to the local copy of that image
    """
    image_path = search_image(query, engine)
    set_wallpaper(image_path)

    return image_path


def query_from_list():
    """
    Choose a random name from the list of queries and set that as wallpaper
    """

    with open(SEARCHES_TXT) as f:
        queries = f.readlines()
        query = random.choice(queries)

    return query


def use_random_image(engine):
    """
    Used to pull an image from one of the queries in the searches.txt file
    """
    query = query_from_list()
    query_to_wallpaper(query + " hot", engine)


def main(query=None, engine='zimg'):

    if query:
        #if you don't add 'hot' you can get all sorts of unwanted images
        query_to_wallpaper(query + " hot", engine)
    else:
        use_random_image(engine)


if __name__ == "__main__":

    #uses a query to search, second param is either 'zimg' or 'bing'
    # main("scarlett johansson", 'bing')

    #pulls a query from a text file instead, calling main() without args
    from time import sleep
    while True:
        main(engine='bing')
        #30 minutes
        sleep(60 * 5)
