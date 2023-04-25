# Spotify-musical-time-machine

it creates a spotify playlist on given date, the date must be in `YYYYMMDD` format. on the given date it scrape top 100 songs of that date from `Billboard.com` and search the name of each song in spotify and creates a playlist and store the song in that plalist.

# installation
you will in need these things:
- `thinter` for `GUI` if you want an `UI`
- `requests` module
- `beautiful soup` for web scraping `from bs4 import BeautifulSoup`
- `spotipy` to use `spotify` api endpoints
- `from spotipy.oauth2 import SpotifyOAuth` for spotify authentication 
- goto `spotify for developer` create account and get the `client_id` and `client_secret`
for more info read the documentation of `spotify api and spotipy`
