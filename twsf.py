import tweepy, re, time, ConfigParser
from urllib import urlopen
from bs4 import BeautifulSoup

config = ConfigParser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

optionsUrl = 'http://booking.sfcinemacity.com/visPrintShowTimes.aspx?visLang=1&visCinemaId=9936'
optionsPage = urlopen(optionsUrl)

soup = BeautifulSoup(optionsPage)

cname = str(soup.findAll('span',{'class':'PrintCinemaName'})[0].next)
current_date = time.strftime("%a %d %b")
info = []

# fetch movies name and showtimes
for td in soup.find_all('td',{'class':'PrintShowTimesFilm'}):
    movie_name = re.sub('\[[^)]*\]', '', td.text).strip()
    date = td.next_element.next_element.next_element.contents[1].text
    if date != current_date : continue
    time = td.next_element.next_element.next_element.contents[2].text
    info.append(movie_name+' '+time)

for i in info:
	api.update_status(status=(cname+"\n"+current_date+"\n"+i))
	print cname+"\n"+current_date+"\n"+i