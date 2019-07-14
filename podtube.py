import os
from flask import Flask, make_response, flash, redirect, render_template, send_from_directory, Response, request, session, abort, url_for
import json
from podgen import Podcast, Episode, Media, Person, Category
import connect
import re
#scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def useDB(cursor):
    use_db = """
    USE database_name
    """
    cursor.execute(use_db)


def get_playlist_id():
    playlistId = "PLqvJuaAfjXbQZEZrIYkNHyd5JYW4peIwE"
    return playlistId



def create_podcast(name, desc, website):
    p = Podcast()
    #if not res:
    p.name = name
    p.description = desc
    p.authors  = [Person("Dawn News", "zarahatkay@dawnnews.com")]
    p.website = website
    p.image = "http://3.15.38.214/zarahatkay/cover_art.png"
    p.language = "en-US"
    p.feed_url = "http://3.15.38.214/zarahatkay"
    p.category = Category("News &amp; Politics")
    p.explicit = False
    return p


def add_episodes(p, response):

    e = p.add_episode()
    e.id = response[1]
    e.title = response[3]
    e.summary = response[4]
    e.publication_date = response[5]
    e.image = "http://3.15.38.214/zarahatkay/cover_art.png" #response[6]
    e.explicit = False
    e.media = Media(response[2],
                    #size=17475653,
                    type="audio/mpeg"  # Optional, can be determined
                                             # from the url
                         #duration=timedelta(hours=1, minutes=2, seconds=36)
                    )
    return p



application = Flask(__name__,static_folder='static')
application.debug = True



@application.route("/zarahatkay")
def server():

    #right now treating podcast id as playlist id
    playlist_id = get_playlist_id()


    db = connect.connect2db()
    cur = db.cursor()
    useDB(cur)

    p = create_podcast("Zara Hat Kay", "Zara Hat Kay Description", "https://www.youtube.com/channel/UCaxR-D8FjZ-2otbU0_Y2grg")

    cur.execute("SELECT * FROM podcast") #WHERE podcast_id = %s", (playlist_id,))
    

    for round in cur:
        add_episodes(p, round)


    p.rss_file('templates/'+playlist_id+'.rss', minimize=True)

    rss_xml = render_template(playlist_id+'.rss')
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


@application.route('/zarahatkay/cover_art.png')
def cover_art():
    return send_from_directory(application.static_folder, "cover_art.png", conditional=True)


@application.route('/zarahatkay/episodes/<epi_id>')
def epiInfo(epi_id):
    mp3filename = epi_id
    full_path = application.static_folder+"/"+mp3filename
    #print(full_path)
    
    file_size = os.stat(full_path).st_size
    start = 0
    length = 10240  # can be any default length you want

    range_header = request.headers.get('Range', None)
    if range_header:
        m = re.search('([0-9]+)-([0-9]*)', range_header)  # example: 0-1000 or 1250-
        g = m.groups()
        byte1, byte2 = 0, None
        if g[0]:
            byte1 = int(g[0])
        if g[1]:
            byte2 = int(g[1])
        if byte1 < file_size:
            start = byte1
        if byte2:
            length = byte2 + 1 - byte1
        else:
            length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)

    rv = Response(chunk, 206, mimetype='audio/mp3', content_type='audio/mp3', direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return rv


@application.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

if __name__ == "__main__":

    application.run(host='0.0.0.0',port=80, threaded=True)
    #application.run()
