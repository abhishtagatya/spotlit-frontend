#!/usr/bin/env python3

""" SpotLit - Front End """

import os
import sys

import requests
from flask import Flask, request, render_template, url_for, redirect
from flask_compress import Compress
from multiprocessing import Value, Process, Queue

app = Flask(__name__)
Compress(app)
version = "v0.3 Alpha"

counter = Value('i', 0)
overlay_limit = 10

@app.route('/')
@app.route('/home', methods=['POST','GET'])
def home():
    """ Renders the front page of the website """

    with counter.get_lock():
        counter.value += 1
        if (counter.value % overlay_limit == 0):
            overlay = True
        else :
            overlay = False

    track_detail = {
    "name" : "Never Gonna Give You Up",
    "artist" : "Rick Astley",
    "album" : url_for('static', filename="img/album_placeholder.jpeg"),
    "spotify_url" : "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC",
    "preview" : None
    }

    return render_template('home.html', track=track_detail, overlay=overlay)

@app.route('/chart')
def chart():
    """ Return Top 3 Charts and their songs """
    limit = 3

    top_chart_song = [
    ('This Is America', 'Childish Gambino', 'open.spotify.com'),
    ('Better Now', 'Post Malone', 'open.spotify.com'),
    ('One Kiss (with Dua Lipa)', 'Calvin Harris, Dua Lipa', 'open.spotify.com')]

    top_chart_playlist = {
    "name" : "Global Top 50",
    "track" : top_chart_song,
    "spotify_url" : "open.spotify.com",
    "image" : url_for('static', filename="img/album_placeholder.jpeg")
    }

    viral_chart_song = [
    ('New Light', 'John Mayer', 'open.spotify.com'),
    ('This Is America', 'Childish Gambino', 'open.spotify.com'),
    ('Toy', 'Netta', 'open.spotify.com')]

    viral_chart_playlist = {
    "name" : "Viral Top 50",
    "track" : viral_chart_song,
    "spotify_url" : "open.spotify.com",
    "image" : url_for('static', filename="img/album_placeholder.jpeg")
    }

    spotlit_chart_song = [
    ('Breezeblocks', 'alt-J', 'open.spotify.com'),
    ('Day 1 O', 'HONNE', 'open.spotify.com'),
    ('Tadow', 'Masego, FKJ', 'open.spotify.com')]

    spotlit_chart_playlist = {
    "name" : "SpotLit Weekly",
    "track" : spotlit_chart_song,
    "spotify_url" : "open.spotify.com",
    "image" : url_for('static', filename="img/album_placeholder.jpeg")
    }

    return render_template('chart.html', charts=(top_chart_playlist, viral_chart_playlist, spotlit_chart_playlist))

@app.route('/playlist')
def playlist():
    """ Return Rendered Playlist HTML """

    selectedPlaylist = {
    "owner"  : "spotit"
    }

    spotlit_chart_song = [
    ('Breezeblocks', 'alt-J', 'open.spotify.com'),
    ('Day 1 O', 'HONNE', 'open.spotify.com'),
    ('Tadow', 'Masego, FKJ', 'open.spotify.com'),
    ('Breezeblocks', 'alt-J', 'open.spotify.com'),
    ('Day 1 O', 'HONNE', 'open.spotify.com'),
    ('Tadow', 'Masego, FKJ', 'open.spotify.com'),
    ('Breezeblocks', 'alt-J', 'open.spotify.com'),
    ('Day 1 O', 'HONNE', 'open.spotify.com')]

    playlist_detail = {
    "name" : "SpotLit Playlist",
    "track" : spotlit_chart_song,
    "spotify_url" : "open.spotify.com",
    "image" : url_for('static', filename="img/album_placeholder.jpeg")
    }

    with counter.get_lock():
        counter.value += 1
        if (counter.value % overlay_limit == 0):
            overlay = True
        else :
            overlay = False

    return render_template('playlist.html', owner=selectedPlaylist['owner'], playlist=playlist_detail, overlay=overlay)

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend', methods=['POST','GET'])
def sendRequest():

    if request.method == 'POST':
        return redirect('home')

@app.route('/about')
def about():
    return render_template('about.html', version=version)

@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', debug=True, port=port)
    sys.exit()
