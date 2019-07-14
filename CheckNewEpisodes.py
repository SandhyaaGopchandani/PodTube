#!/usr/local/bin/python3

from apiclient.discovery import build
import connect
from Y2Mp3 import Y2Mp3
from apiclient.discovery import build


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyD3NpweWb_NIxnq7kXMrRY4YQao29gqvlQ"


def get_youtube_obj(api_service_name, api_version, developerKey):
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    return youtube


def useDB(cursor):
    use_db = """
    USE database_name
    """
    cursor.execute(use_db)


def createTable(cursor):
    create_table="""
    create table podcast(
    podcast_id varchar(30),
    epi_id varchar(30),
    epi_url varchar(100),
    epi_title varchar(200),
    epi_summary varchar(1000),
    epi_pub_date varchar(50),
    epi_thumbnail_link varchar(100),
    downloaded int
    )
    """
    cursor.execute(create_table)



def get_channel_id():
	channelId = "UCaxR-D8FjZ-2otbU0_Y2grg"
	return channelId


def get_playlist_id():
	playlistId = "PLqvJuaAfjXbQZEZrIYkNHyd5JYW4peIwE"
	return playlistId


def search_video(video_id="8buCsouQEic"):
    youtube = get_youtube_obj(api_service_name, api_version, DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    return response


def search_youtube(channelId):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    youtube = get_youtube_obj(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        channelId=channelId,
        order="date",
        q="Zara Hat Kay",
        type="video",
        videoDuration="long"
        #parser = None
    )
    response = request.execute()

    return response


def getVideoLink(id):
    return "https://www.youtube.com/watch?v="+id


def getEpisodelink(epid):
    return "http://3.15.38.214/zarahatkay/episodes/"+str(epid)+".mp3"



def checkNewEpisodes(response, in_video_id=None):
	#channelId = get_channel_id()
	#response = search_youtube(channelId)
        if in_video_id is None:
            epi_id = response["items"][0]["id"]["videoId"]
        else:
            epi_id = in_video_id
        epi_title = response["items"][0]["snippet"]["title"]
        epi_summary = response["items"][0]["snippet"]["description"]
        epi_pubdate = response["items"][0]["snippet"]["publishedAt"]
        playlist_id = get_playlist_id()
        video_url = getVideoLink(epi_id)
        epi_url = getEpisodelink(epi_id)
        epi_thumbnail_link = response["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        
        downloader = Y2Mp3()
        db = connect.connect2db()
        cur = db.cursor()
        useDB(cur)
        
        res  = cur.execute("SELECT epi_id FROM podcast WHERE epi_id = %s", (epi_id,))
        
        if not res:
            downloader.startDownload(video_url)
            downloaded = 1
            cur.execute(
                    'INSERT INTO podcast (podcast_id, epi_id, epi_url, epi_title, epi_summary, epi_pub_date, epi_thumbnail_link, downloaded) VALUES ( "{}","{}","{}","{}","{}","{}","{}","{}")'.format(playlist_id, epi_id, epi_url, epi_title, epi_summary, epi_pubdate, epi_thumbnail_link,  downloaded))
            db.commit()
            
        print("downloaded and inserted to the database")

def deleteFromDB():
    playlist_id = get_playlist_id()
    print(playlist_id)
    db = connect.connect2db()
    cur = db.cursor()
    useDB(cur)
    
    cur.execute("""Delete from podcast where podcast_id = 'PLqvJuaAfjXbQZEZrIYkNHyd5JYW4p'""")
    db.commit()
    #res = cur.execute("SELECT * FROM podcast WHERE podcast_id = %s", (playlist_id,))
    cur.execute("SELECT * FROM podcast")
    
    for round in cur:
        print(round)
if __name__ == "__main__":
	#db = connect.connect2db()
	#cur = db.cursor()
	#useDB(cur)
	#createTable(cur)
        channelId = get_channel_id()
        response = search_youtube(channelId)
        checkNewEpisodes(response)
        #deleteFromDB()

