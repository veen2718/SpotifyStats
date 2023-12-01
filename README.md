# SpotifyStats

A python script that gives detailed statistics about your Spotify history

## Instructions

Download the latest release from the release page.
Extract the zip.

### Downloading Spotify Data

Go to https://www.spotify.com/ca-en/account/privacy#/
Request your Account Data. Within 5 days you should get an email containing a zip with your data. 
There is a folder in that zip called 'Spotify Account Data'. That folder should contain several files including one or more files named similar to 'StreamingHistory0.json'. 
Copy the entire folder into the folder with the python script. 

### Getting Spotify API Client ID and Client Secret

If you do not want to use the Spotify API and only want to get data from downloading it from Spotify's website, you can change the value of the ``useAPI`` in the vars.py file to False


Go to https://developer.spotify.com/dashboard/applications

Log in with your spotify account

Click on 'create an app', and pick an 'App name' and 'App description', the name and description do not matter

After creation, you can see your Client ID and Client Secret, which you will need in the next step

### Setting up the python script

Do all the following steps if you want to use the Spotify API:

- In the release folder, create a file called 'apikeys.py'

- in the file add the following lines of code

    ```python

    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    ```

- Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your Client ID and Secret from earlier. 

Do the next step regardless of whether or not you want to use the Spotify API:

- Run ``pip  install -r requirements.txt``, which will install required libraries


### Usage

Run main.py, and a folder will be created called *stats*. In that folder there shoud be an *artists.txt* and *tracks.txt*, containing a table with the data. Once table is generated, the 'Spotify Account Data' folder will be deleted,and a history.json will be created to store the data. 

Later, you may request your data again, and copy the 'Spotify Account Data' folder into the SpotifyStats folder. Running main.py again will merge any new history from the 'Spotify Account Data' with your old history.

Every time you run main.py, it will make an API call, and add the 50 most recently played songs to the history.json. Because of limits of the Spotify API you cannot get the entire history from the API, so I recommend that you use a command scheduler to schedule the main.py script to run frequently. 

### vars.py
There are multiple variables the user can change in the vars.py file

`mMin`: This is the number of minutes a song will have to play before the song counts as a track

`getDownloadedData`: If this is true, it will check the Spotify Account Data folder and read data from there, else it will read from history.json. If the Spotify Account Data folder has been deleted, it will act as though this is false.

`sortBy`: If this is set to 0, it will sort the table by the number of times a track is played. If this is set to 1, it will sort the table by the number of minutes a track is played for. 

`useAPI`: If this is False, will not use the Spotify API, and will just use downloaded data
## Current Features

- Generate table for artist data including artist name, minutes played, times their tracks are played
- Generate table for track data including track name, artist of track, minutes played, times the track is played
- Get data from Spotify API in addition to downloaded data

## Upcoming Features

- GUI
- Graph with interest in songs/artists over time