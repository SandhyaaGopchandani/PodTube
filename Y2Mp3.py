import youtube_dl


class Y2Mp3:
    def __init__(self):
        self.ydl = youtube_dl.YoutubeDL(self.getOptions())

    def hook(self, d):
        if d['status'] == 'finished':
            print('downloading done. Converting...')

    def getOptions(self):
        return {
            'outtmpl': 'static/%(id)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [self.hook],
        }

    def startDownload(self, url):
        self.ydl.download([url])
