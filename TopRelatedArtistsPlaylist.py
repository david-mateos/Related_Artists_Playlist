#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a playlist from the related
artists of the user's top artists. 

Note: script must have a client id and app secret
from spotify to accept the scopes.
Log in to: https://developer.spotify.com/dashboard/applications
and copy info from 'Edit Settings' tab

Copy and paste the url from the authentication bounce 
into the console once permissions are accepted.

@author: davidmateos
"""
import spotipy
import spotipy.util as util

USERNAME= '' #the user's id
SCOPE= 'playlist-modify-public,user-top-read,playlist-modify-public' 
CLIENT_ID=''
CLIENT_SECRET= ''
REDIRECT_URI= 'https://localhost:8080'

util.prompt_for_user_token(username=USERNAME,
                           scope=SCOPE,
                           client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           redirect_uri=REDIRECT_URI)

token = util.prompt_for_user_token(USERNAME, SCOPE)
sp = spotipy.Spotify(auth=token)
sp.trace = False

playlist_name = 'Listen to This!' # name the playlist!
playlist_description ='Made from the tracks of your top artists related artists'
t_range= 'medium_term' # using medium term listening time scale


if token:
    # S1: get user's top 10 artists and their related counterparts
    top_artists = sp.current_user_top_artists(time_range=t_range, limit=10)
    
    artists= [] 
    related_artists= []
    tracks= []
    
    for i, item in enumerate(top_artists['items']):
        
        artists.append(item['id']) 
        related_artist= sp.artist_related_artists(artists[i])['artists'][0]['id']
        related_artists.append(related_artist)
    
    # S2: get the top 2 tracks for each top related artist
    for i, id in enumerate(related_artists):
    
        top_tracks1= sp.artist_top_tracks(id, country='US')['tracks'][0]
        top_tracks2= sp.artist_top_tracks(id, country='US')['tracks'][1]
        track_ids1= top_tracks1['id']
        track_ids2= top_tracks2['id']
        tracks.append(track_ids1)
        tracks.append(track_ids2)
    
    # S3: Create the Playlist
    playlist= sp.user_playlist_create(USERNAME,
                                      playlist_name,
                                      public=True,
                                      description=playlist_description)
    
    new_playlist_id= sp.current_user_playlists()['items'][0]['id']
    
    # S4: Fill playlist with top related artist tracks 
    sp.user_playlist_add_tracks(USERNAME, new_playlist_id, tracks)

else:
    print("Could not get token for", USERNAME)
