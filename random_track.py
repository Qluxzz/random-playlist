#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse
import random
import math
import datetime
import configparser
import spotipy
import spotipy.util as util

def get_query(arguments):
    query = ''
    if 'genre' in arguments and arguments['genre'] != None:
        query += ' genre:' + arguments['genre']
    if 'year' in arguments and arguments['year'] != None:
        query += ' year:' + arguments['year']
    if 'artist' in arguments and arguments['artist'] != None:
        query += ' artist:' + arguments['artist']
    return query

def add_tracks_to_playlist(_spotipy, username, playlist_id, track_ids):
    if len(track_ids) > 100:
        ids =  []
        for amount in range(0, len(track_ids), 100):
            if amount + 100 > len(track_ids):
                ids = track_ids[amount:]
            else:
                ids = track_ids[amount:amount + 100]
            _spotipy.user_playlist_add_tracks(username, playlist_id, ids)
    else:
        _spotipy.user_playlist_add_tracks(username, playlist_id, track_ids)

def get_random_character():
    return chr(random.randint(0, 0x10FFFF))

def get_tracks(_spotipy, amount, username, arguments):
    print(arguments)
    """ Gets amount of tracks of genre and adds them to a playlist """
    ids = set()
    query = get_query(arguments)

    while len(ids) < amount:
        try:
            results = _spotipy.search(q=query, type='track', limit=1)

            if 'tracks' not in results or 'total' not in results['tracks']:
                continue

            total = results['tracks']['total']
            if total < amount:
                print('Not enough tracks for a playlist')
                return

            results = _spotipy.search(
                q=query,
                type='track',
                limit=1,
                offset=random.randint(0, (total, 100000)[total > 100000])
            )
        except spotipy.client.SpotifyException as ex:
            print('Failed to find tracks matching the criteria')
            print(ex)
            return
        except TypeError as ex:
            print(ex)

        tracks = results['tracks']['items']
        number_of_tracks = len(tracks)

        if number_of_tracks >= 1:
            track_id = tracks[random.randint(0, number_of_tracks - 1)]['id']
            ids.add(track_id)
    # Create a new playlist
    playlistname = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if 'playlistname' in arguments and arguments['playlistname'] != None:
        playlistname = arguments['playlistname']

    result = _spotipy.user_playlist_create(username, playlistname, public=False)
    add_tracks_to_playlist(_spotipy, username, result['id'], list(ids))

def main():
    """ Main function """
    parser = argparse.ArgumentParser(description='Creates random spotify playlist')
    parser.add_argument('--amount', help='Amount of tracks to add', type=int)
    parser.add_argument('--username', help='Spotify Username')
    parser.add_argument('--artist', help='Artist')
    parser.add_argument('--genre', help='Music genre')
    parser.add_argument('--year', help='Year, can be a single year or a range as ex. 1995-2000')
    parser.add_argument('--playlistname', help='Name of playlist, default is the current date and time')

    # If no arguments were supplied
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
        sys.exit()

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('settings.ini')

    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(
        args.username,
        scope,
        client_id=config['DEFAULT']['SPOTIPY_CLIENT_ID'],
        client_secret=config['DEFAULT']['SPOTIPY_CLIENT_SECRET'],
        redirect_uri=config['DEFAULT']['SPOTIPY_REDIRECT_URI']
    )
    _spotipy = spotipy.Spotify(auth=token)
    get_tracks(_spotipy, int(args.amount), args.username, vars(args))

if __name__ == "__main__":
    main()