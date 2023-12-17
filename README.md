# Unwrapped - Spotify Stats

A python script that gives detailed statistics about your Spotify history

## Instructions

Download the latest release from the release page.
Extract the zip.

### Downloading Spotify Data

Go to https://www.spotify.com/ca-en/account/privacy#/
Request your Account Data. Within 5 days you should get an email containing a zip with your data. 
There is a folder in that zip called 'Spotify Account Data'. That folder should contain several files including one or more files named similar to 'StreamingHistory0.json'. 
Copy the entire folder into the 'Unwrapped' folder with the python script. 

### Getting Spotify API Client ID and Client Secret

If you do not want to use the Spotify API and only want to get data from downloading it from Spotify's website, you can change the value of the ``useAPI`` in the vars.py file to False


Go to https://developer.spotify.com/dashboard/applications

Log in with your spotify account

Click on 'create an app', and pick an 'App name' and 'App description', the name and description do not matter

After creation, you can see your Client ID and Client Secret, which you will need in the next step

### Getting Google Drive API

Note: The API can randomly expire. This means that if you are automating this on multiple devices as suggested, you may need to manually sign-in again. 

The purpose of this is so that you can have this program automated on multiple devices. For example, if you have a laptop and a desktop, you can have the program automated on both devices, so the script can still collect data from spotify when one device isn't being used. Alternatively, if you have something like a Raspberry Pi, you can use that purely for automation, and you can access and view the data from a different computer. 

Go to https://console.cloud.google.com/, and create a project. In the dashboard, navigate to 'Library' and then search for the "Google Drive API" and enable it. 

Go to OAuth Consent Screen, and set user type to external. Then click continue, and choose any app name, and your support email. You don't need to choose a logo file, and leave the App domain section blank. Put your email under Developer Contact information. Save and continue.

Now in scopes, click 'ADD OR REMOVE SCOPES'. Under Manually add scopes, paste this entire url: "https://www.googleapis.com/auth/drive.file", make sure to keep the https://, and click 'ADD TO TABLE' and then 'UPDATE'. Click Save and Continue. 

Now in Test users, click Add Users. Enter the gmail address you want your data to be backed up to, and click enter. (This gmail account can be the same one that you are using to make this app) Click Save and Continue. 

Now, in the sidebar, click Credentials. Now click 'CREATE CREDENTIALS' and click 'OAuth client ID'. For application type, select Desktop App. For Name, put whatever. Click CREATE. There will be a popup, saying OAuth client created. Click download json, and make sure that you have renamed it as 'googleapi.json' and that you have saved it in the Unwrapped folder. 


Now that you have the credentials, you can run main.py, It will say 'Please visit this URL to authorize this application' or just open a link directly in your browser.When the link is opened it will say something along the lines of 'This app hasn't been verified by google'. This is normal, and you know the app is completely safe as you have just set up up in the google cloud console. Just continue, and then sign into a gmail account that you made a 'Test User', in a previous step. If you get a 'something went wrong', copy the link given into an incognito tab and try again. From there you should be able to give this app permission to edit its own files inside your google drive. 

### Setting up the python script

Do all the following steps if you want to use the Spotify API:

- In the release folder, create a file called 'apikeys.py'

- in the file add the following lines of code

    ```python

    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    ```

- Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your Spotify Client ID and Secret from earlier. 

Do the next step regardless of whether or not you want to use the Spotify API:

- Run ``pip  install -r requirements.txt``, which will install required libraries


### Usage

Run main.py, and a folder will be created called *stats*. In that folder there shoud be an *artists.txt* and *tracks.txt*, containing a table with the data. Once table is generated, the 'Spotify Account Data' folder will be deleted,and a history.json will be created to store the data. 

Later, you may request your data again, and copy the 'Spotify Account Data' folder into the SpotifyAnalyze folder. Running main.py again will merge any new history from the 'Spotify Account Data' with your old history.

Every time you run main.py, it will make an API call, and add the 50 most recently played songs to the history.json. Because of limits of the Spotify API you cannot get the entire history from the API, so I recommend that you use a command scheduler to schedule the main.py script to run frequently. 


### Automation
I highly recommend that you automate this script to run frequently. This is because through Spotify's API you can only get the 50 most recently played songs from a user's history. This is why you requested and downloaded your data from Spotify because that way you have a lot more of your history. But by frequentely calling Spotify's API and storing the songs when we can, we can build a near complete record of streaming history which can then be analyzed by this script. For Linux, MacOS or WSL you can use Crontab to schedule this file to run, or on MacOS you can use Automator and on Windows you can use Task Scheduler. 


### vars.py
There are multiple variables the user can change in the vars.py file

`mMin`: This is the number of minutes a song will have to play before the song counts as a track

`getDownloadedData`: If this is true, it will check the Spotify Account Data folder and read data from there, else it will read from history.json. If the Spotify Account Data folder has been deleted, it will act as though this is false.

`sortBy`: If this is set to 0, it will sort the table by the number of times a track is played. If this is set to 1, it will sort the table by the number of minutes a track is played for. 

`useAPI`: If this is False, will not use the Spotify API, and will just use downloaded data

`useGoogleDrive`: If this is True, it will use Google Drive for backing up the history.json

### Updating to newer version
When updating to a newer version, simply copy the history.json file into the folder with the new release 

## Current Features

- Generate table for artist data including artist name, minutes played, times their tracks are played
- Generate table for track data including track name, artist of track, minutes played, times the track is played
- Get data from Spotify API in addition to downloaded data

## Upcoming Features

- GUI
- Graph with interest in songs/artists over time
- Android App