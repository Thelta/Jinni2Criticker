import sys
import argparse
import imdbpie
from helium.api import *
import json
import time

moviesString = """[
  ["Evangelion 1.01: You Are (Not) Alone",2007,"Movie",8],
  ["Memento",2000,"Movie",7],
  ["300",2006,"Movie",7],
  ["God Bless America",2011,"Movie",8],
  ["The Raid",2011,"Movie",8],
  ["Kill Bill 2",2004,"Movie",8],
  ["Kill Bill 1",2003,"Movie",8],
  ["V For Vendetta",2005,"Movie",8],
  ["Person of Interest",2011,"TV-Series",10],
  ["Suits",2011,"TV-Series",9],
  ["Veronica Mars",2004,"TV-Series",10]
]"""

def AllArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-username", required = True, help = "Your Criticker.com username")
	parser.add_argument("-password", required = True, help = "Your Criticker.com password")
	return parser.parse_args()
	

def Login(username, password):
	go_to("https://www.criticker.com/signin.php")
	write(username, into = "User Name")
	write(password, into = "Password")
	click(S("#si_submit"))

def SearchMovie(movie):
	imdbSearch = imdb.search_for_title(movie[0])
	for imdbMovie in imdbSearch:
		if int(imdbMovie['year']) == movie[1]:
			break
	imdbMovie = imdb.get_title_by_id(imdbMovie['imdb_id'])
	searchString = imdbMovie.title 
	yearSuffix = " (" + imdbMovie.release_date[:4] + ")"
	click(S("#i_searchbox"))
	write(searchString, into = S("#i_searchbox"))
	try:
		select("All", "Movies")
	except LookupError:
		pass
	click("Go")
	search = find_all(Link(searchString + yearSuffix))
	if len(search) == 0:
		print("Can't find: " + searchString + yearSuffix)
		return
	linkIndex = 0
	for link in search:
		if not "https://www.criticker.com" in link.href:
			linkIndex += 1
		else:
			break
			
	if linkIndex >= len(search):
		print("Can't find: " + searchString)
		return
		
	click(search[linkIndex])
	
	SubmitMovieScore(movie)
	
def SubmitMovieScore(movie):
	search = find_all(Text("ranked on"))
	if len(search) == 0:
		write(movie[3] * 10, into="Your Rating")
		click("Submit")
		
if __name__ == "__main__":
    
	movies = json.loads(moviesString)
	args = AllArgs() 

	start_chrome("www.criticker.com")
	Login(args.username, args.password)
	
	imdb = imdbpie.Imdb(anonymize=True)

	for movie in movies:
		if movie[2] == "Movie":
			SearchMovie(movie)		