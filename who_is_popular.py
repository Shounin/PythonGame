from bs4 import BeautifulSoup
import urllib.request
import re
from pprint import pprint

# This is a very slow program that gives you a list of the actors who appear most in these
# movies provided by the Internet Movie Database top 250 (http://www.imdb.com/chart/top).
# The user can modify the list of movies by filtering the year gap.
# At last, the user can get a list of movies a specific actor has appeared in.
def who_is_popular(max, year_min=0, year_max=5000):
    print('Processing...')
    page = urllib.request.urlopen('http://www.imdb.com/chart/top')
    soup = BeautifulSoup(page)
    popularity = {}
    
    # Getting all the links
    lis = [ link.get('href') for link in soup.find_all('a')
            if '/title/tt' in link.get('href') ]
    lis = [ x for x in lis[::2] ]

    # Getting data for the popularity list.
    counter = 0
    for link in lis:
        if counter >= int(max):
            break
        movie = get_movie(link.split('?')[0])
        if int(movie[-5:-1]) >= int(year_min) and int(movie[-5:-1]) <= int(year_max):
            actors = get_actors(link.split('?')[0])
            for actor in actors:
                popularity[actor] = popularity.get(actor, []) + [movie]
            counter += 1
    
    # The most popular actors.
    num = int(input('How long do you want the popularity list of actors to be? \n'))
    for n, act in enumerate(sorted(popularity, key=lambda k: len(popularity[k]), reverse=True)):
        if n < num:
            if len(popularity[act]) > 1:
                print('{} has been in {} movies.' .format(act, len(popularity[act])))
            else:
                print('{} has been in {} movie.' .format(act, len(popularity[act])))

    # Movies for specific actors.
    while input('Would you like to get a list of movies for specific actor? (y/n) \n') is 'y':
        dude = input('Enter name of actor to see the movies he has been in\n')
        if dude in popularity.keys():
            if len(popularity[dude]) > 1:
                print('{} has been in these movies: ' .format(dude))
                [ print(x) for x in popularity[dude] ]
                print()
            else:
                print('{} has been in this movie: ' .format(dude))
                [ print(x) for x in popularity[dude] ]
                print()
        else:
            print('The name {} was not found' .format(dude))


# Finding the name of a movie.
def get_movie(url):
    soup = BeautifulSoup(urllib.request.urlopen('http://imdb.com' + url))
    return soup.title.text[:-7]

# Finding actors in a movie.
def get_actors(url):
    full_cast = 'fullcredits?ref_=tt_cl_sm#cast'
    soup = BeautifulSoup(urllib.request.urlopen('http://imdb.com' + url + full_cast))
    actors = soup.find_all("td", {"itemprop":"actor"})
    return set([x.text.strip() for x in actors])



# Function
max = input('Enter number of movies to process\n')
ans = input('Do you want to filter the movies by year? (y/n)\n')
if ans is 'y':
    year_min = input('The year minimum: \n')
    year_max = input('The year maximum: \n')
    who_is_popular(max, year_min, year_max)
else:
    who_is_popular(max)
