import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError,RequestError
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

# from pepper import *
import configparser

def read_config_file(file_path):
    # Create a ConfigParser instance
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read('setup.txt')
    return config['default']


file_path = "setup.txt"
config_data = read_config_file(file_path)
# Extract values using the section name and key
client_id = config_data.get('client_id')
client_secret = config_data.get('client_secret')
device_name = config_data.get('device_name')
redirect_uri = config_data.get('redirect_uri')
username = config_data.get('username')
scope = config_data.get('scope')


# Print the extracted values
print("client_id:", client_id)
print("client_secret:", client_secret)
print("device_name:", device_name)
print("redirect_uri:", redirect_uri)
print("username:", username)
print("scope:", scope.split())  # Split the scope string into a list


"""
To run this script, you must have a file in this directory called 'setup.txt'
In this file, enter all of the values of the required variables in the following format:

client_id=XXXXXXXX
client_secret=XXXXXXX
device_name=Jake's iMac
redirect_uri=https://example.com/callback/
username=jakeg135
scope=user-read-private user-read-playback-state user-modify-playback-state
"""

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
print(devices)
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        print("Hello world")
        break

# Setup microphone and speech recognizer
r = Recognizer()
m = None
input_mic = 'Headset (Infinity GLIDE 4000 Hands-Free AG Audio)'  # Use whatever is your desired input
# input_mic = 'Microphone Array (Realtek(R) Audio)'  # Use whatever is your desired input
for i, microphone_name in enumerate(Microphone.list_microphone_names()):
    if microphone_name == input_mic:
        print("hello word x2 - ",microphone_name)
        m = Microphone(device_index=i)
        break

while True:
    """
    Commands will be entered in the specific format explained here:
     - the first word will be one of: 'album', 'artist', 'play'
     - then the name of whatever item is wanted
    """
    with m as source:
        r.adjust_for_ambient_noise(source=source)
        audio = r.listen(source=source)

    command = None
    try:
        command = r.recognize_google(audio_data=audio).lower()
    except RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except UnknownValueError:
        continue
    

    print(command)
#     words = command.split()
#     if len(words) <= 1:
#         print('Could not understand. Try again')
#         continue

#     name = ' '.join(words[1:])
#     try:
#         if words[0] == 'album':
#             uri = get_album_uri(spotify=spotify, name=name)
#             play_album(spotify=spotify, device_id=deviceID, uri=uri)
#         elif words[0] == 'artist':
#             uri = get_artist_uri(spotify=spotify, name=name)
#             play_artist(spotify=spotify, device_id=deviceID, uri=uri)
#         elif words[0] == 'play':
#             uri = get_track_uri(spotify=spotify, name=name)
#             play_track(spotify=spotify, device_id=deviceID, uri=uri)
#         else:
#             print('Specify either "album", "artist" or "play". Try Again')
#     except InvalidSearchError:
#         print('InvalidSearchError. Try Again')