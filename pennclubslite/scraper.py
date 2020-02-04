from bs4 import BeautifulSoup
import urllib.request
import requests
from .models import Club, Category



def get_html(url):
    """
    Retrieve the HTML from the website at `url`.
    """
    return requests.get(url)

def get_clubs_html():
    """
    Get the HTML of online clubs with Penn.
    """
    url = 'https://ocwp.apps.pennlabs.org'
    return get_html(url).text

def soupify(html):
    """
    Load HTML into BeautifulSoup so we can extract data more easily
    Note that for the rest of these functions, whenever we refer to a "soup", we're refering
    to an HTML document or snippet which has been parsed and loaded into BeautifulSoup so that
    we can query what's inside of it with BeautifulSoup.
    """
    return BeautifulSoup(html, "html.parser") 


def get_elements_with_class(soup, elt, cls):
    """
    Returns a list of elements of type "elt" with the class attribute "cls" in the
    HTML contained in the soup argument.
    For example, get_elements_with_class(soup, 'a', 'navbar') will return all links
    with the class "navbar". 
    Important to know that each element in the list is itself a soup which can be
    queried with the BeautifulSoup API. It's turtles all the way down!
    """ 
    return soup.findAll(elt, {'class': cls})

def get_clubs(soup):
    """
    This function should return a list of soups which each correspond to the html
    for a single club.
    """
    # clubs have element type "div" and class "box"
    return get_elements_with_class(soup, 'div', 'box')

def get_club_name(club):
    """
    Returns the string of the name of a club, when given a soup containing the data for a single club.
    We've implemented this method for you to demonstrate how to use the functions provided.
    """
    elts = get_elements_with_class(club, 'strong', 'club-name')
    if len(elts) < 1:
        return ''
    return elts[0].get_text()

def get_club_description(club):
    """
    Extract club description from a soup of 
    """
    descriptions = get_elements_with_class(club, 'em', '')
    if len(descriptions) < 1:
        return ''
    return descriptions[0].get_text()

def get_club_tags(club):
    """
    Get the tag labels for all tags associated with a single club.
    Return the tag labels as a string array
    """
    tags = get_elements_with_class(club, 'span', 'tag is-info is-rounded')
    tag_names = []
    for t in tags:
        tag_names.append(t.get_text())
    return tag_names

def store_tags(tags, club):
    """
    Input: tags - string list of tags; club - Club object
    Loops through tags and queries db to check whether each tag already exists.
    If the tag exists, directly establish new many-to-many relationship with Club object;
    if not, create new Category object with tag string first
    """
    for t in tags:
        # query db to find tag if it exists already
        existing_tag = Category.objects.filter(tag=t)
        if existing_tag.exists():
            # establish relationship between club and first entry of queryset if it's not empty
            existing_tag[0].clubs.add(club)
        else:
            # create new tag if it doesn't already exist in db
            new_category = Category(tag=t)
            new_category.save()
            new_category.clubs.add(club)
    return

def store_clubs():
    """
    Retrieves name, description and tags of all clubs. Creates new Club object
    with club name and description. Establishes many to many relationship with tags
    by calling store_tags()
    """
    clubs = get_clubs(soupify(get_clubs_html()))
    for c in clubs:
        c_name = get_club_name(c)
        c_description = get_club_description(c)
        c_tags = get_club_tags(c)

        # create new Club object and save it to database
        new_club = Club(club_name=c_name, description=c_description)
        new_club.save()        
        store_tags(c_tags, new_club)


