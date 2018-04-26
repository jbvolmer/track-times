#infinite chill / 2017
all: clean tracklists run

tracklists: tracklists.py
	cp tracklists.py tracklists
	chmod u+x tracklists

run:
	./tracklists times.txt titles.txt tracklist.txt

clean:
	rm -f tracklists 
	