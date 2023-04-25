import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import *
from tkinter import messagebox

def create():

    year = str(year_entry.get())
    month = str(month_entry.get())
    date = str(day_entry.get())
    songs = []
    song_uri =[]
    playlist_id = ''

    # getting html code to perform webscraping

    response = requests.get(f'https://www.billboard.com/charts/hot-100/{year}-{month}-{date}/')
    print(response.raise_for_status())
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all('h3', id= 'title-of-a-story', class_=['c-title a-no-trucate', 'a-font-primary-bold-s'])

    for name in headings:
        song = name.text.strip()
        songs.append(song)

    # setting up spotify api (spotify for developers)

    scope = 'playlist-modify-public'
    client_id = 'e98c02f699aa4eafaa67c4c44e1aebfc'
    client_secret = '3794686269c64bfdbed5966a24dc789a'

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect_uri='https://example.org/callback',
            show_dialog=True,
            cache_path='token.txt'
        )
    )

    user_id = sp.current_user()['id']

    # getting songs uri
    for name in songs[2:]:
        result = sp.search(q=f'track:{name}, year:{year}', type='track')
        try:
            uri = result['tracks']['items'][0]['uri']
            song_uri.append(uri)
        except IndexError:
            # print('skip')
            pass

    ### creating playlist
    playlist_name = f"{year}-{month}-{date} Billboard 100"
    playlist_description = "A description of my new playlist"
    sp.user_playlist_create(user=user_id,
                            name=playlist_name,
                            public=True,
                            description=playlist_description)

    playlists = sp.user_playlists(user_id)

    ### getting the playlist id for currently created playlist
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                # print(f"Playlist name: {playlist['name']}\nPlaylist ID: {playlist['id']}")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    ### adding songs to playlist
    for add in song_uri:
        # print(add)
        sp.playlist_add_items(playlist_id, [add])

    messagebox.showinfo('Woo Hoo!!',message="Playlist created")






window = Tk()
window.title('Spotify Playlist Creator')
window.config(pady=50,padx=50, bg='white')
canvas = Canvas(width=256, height=144, bg='white', highlightthickness=0)
photo =PhotoImage(file='Spotify-Logo-resized.png')
canvas.create_image(127,72, image=photo)
canvas.grid(row=0,column=0,columnspan=3)

year_label = Label(text='Year', font=('Montserrat',15), bg='white', highlightthickness=0)
year_label.grid(row=1,column=0)
year_entry = Entry(width=9, highlightthickness=0)
year_entry.grid(row=3,column=0)

month_label = Label(text='Month', font=('Montserrat',15), bg='white', highlightthickness=0)
month_label.grid(row=1,column=1)
month_entry = Entry(width=9, highlightthickness=0)
month_entry.grid(row=3,column=1)

day_label = Label(text='Date', font=('Montserrat',15), bg='white', highlightthickness=0)
day_label.grid(row=1,column=2)
day_entry = Entry(width=9, highlightthickness=0)
day_entry.grid(row=3,column=2)

bnt_img = PhotoImage(file='output-onlinepngtools.png')
button = Button(image=bnt_img, bg='white', highlightthickness=0, command=create)
button.grid(row=4,column=1,columnspan=1, pady=10)

messagebox.showinfo('Reminder',message="Fill date in 2022/05/18 format")


window.mainloop()


