"""
Written for Python 2.7 on Windows 7x64


Some other searches, as featured in several subreddit sidebars are located in a
text file called searches.txt, which is just a list a names from subreddits like
/r/gentlemanboners

ISSUES:
    * If a request.get call fails, the whole thing crashes.
        + Handle exceptions
    * The search results are always the first page, so if you use this script
      too often, you'll always have the same pool of images
        + Figure out how to go to next page of search results,
          or get more images in one query

TODO:
    * Add ignore urls, so you don't get the same less desirable watermarks
    * Some sort of file organization or limit. Right now, there's not limit on
      the images it saves and keeps on your harddrive
    * Size limits. Can be any size deemed 'large' by the engine. It'd be nice
      to be able to specify dimensions
"""


import ctypes, random, re, os, itertools

#both of these are on pip, I'm sure
import requests, bs4


SEARCHES_TXT = r"searches.txt"
IMAGE_FILENAME = r"wallpaper.jpg"
IMAGE_DIR = r"c:/images/"

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
        image_url = parse_zimg_for_image_url(parsed_query)
    elif engine == 'bing':
        image_url = parse_bing_for_image_url(parsed_query)
    image_path = save_image(image_url, query)

    return image_path

#from http://stackoverflow.com/a/1131255/541208
def md5_for_file(f, block_size=2**20):
    """
    Gets the md5 representation of the file, used for checking for file duplicates
    """
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


#parse for image
def parse_zimg_for_image_url(query):
    """
    Pulls all the image links from a Z-Img.com page, which is just a nice wrapper
    for the Google Image Search
    """
    print 'Using z-img.com as a search engine'
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
    print 'Using bing.com as a search engine'
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


#http://snipplr.com/view.php?codeview&id=41834
def unique_file_name(file):
    ''' Append a counter to the end of file name if
    such file already exist.'''
    if not os.path.isfile(file):
        # do nothing if such file doesn exists
        return file
    # test if file has extension:
    if re.match('.+\.[a-zA-Z0-9]+$', os.path.basename(file)):
        # yes: append counter before file extension.
        name_func = \
            lambda f, i: re.sub('(\.[a-zA-Z0-9]+)$', '_%i\\1' % i, f)
    else:
        # filename has no extension, append counter to the file end
        name_func = \
            lambda f, i: ''.join([f, '_%i' % i])
    for new_file_name in \
            (name_func(file, i) for i in itertools.count(1)):
        if not os.path.exists(new_file_name):
            return new_file_name


def save_image(image_url, query=None):
    """
    Saves the given image_url and returns the local file path that it was
    saved to.
    """
    if not os.path.exists(IMAGE_DIR): os.makedirs(IMAGE_DIR)

    #use the query as a filename if possible, otherwise use preset image_path
    if not query:
        image_path = IMAGE_FILENAME
        proper_image_path = clean_query_for_filepath(image_path)
    else:
        proper_image_path = clean_query_for_filepath(query)

    with open(proper_image_path, 'wb') as f:
        headers = {'user-agent': "z-img-desktop-updater"}
        r = requests.get(image_url, headers=headers)
        f.write(r.content)
        print "Saved image to:", proper_image_path

    return proper_image_path

def clean_query_for_filepath(query):
    #replace spaces and non filename chars
    dirty_string = query.replace(' ', '_')
    keepcharacters = ('.','_')
    image_path = "".join(c for c in dirty_string if c.isalnum() or c in keepcharacters).rstrip()
    if not image_path.endswith('.jpg'):
        image_path = image_path + '.jpg'
    possible_image_path = os.path.join(IMAGE_DIR, image_path)
    proper_image_path = unique_file_name(possible_image_path)

    return proper_image_path


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
    else:
        print "Sucessfully set wallpaper to", image_path


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
    main(engine='bing')

    #pulls a query from a text file instead, calling main() without args
    # from time import sleep
    # while True:
    #     main(engine='bing')
    #     #5 minutes
    #     sleep(60 * 5)
