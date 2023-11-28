# SpotifyStats

A python script that gives detailed statistics about your Spotify history

## Instructions

Download the latest package from the packages page.
Extract the package.

Go to https://www.spotify.com/ca-en/account/privacy#/, and request your Account Data. Within 5 days you should get an email containing a zip with your data. There is a folder in that zip called 'Spotify Account Data'. That folder should contain several files including one or more files named similar to 'StreamingHistory0.json'. Copy the entire folder into the folder with the python script. Run main.py, and a folder will be creaed called *stats*. In that folder there shoud be an *artists.txt* and *tracks.txt*, containing a table with the data. Once table is generated, feel free to delete the 'Spotify Account Data' folder, a history.json will be created to store the data. 

## Current Features

- Generate table for artist data including artist name, minutes played, times their tracks are played
- Generate table for track data including track name, artist of track, minutes played, times the track is played

## Upcoming Features

- Use spotify API to get data
- GUI
- Graph with interest in songs/artists over time