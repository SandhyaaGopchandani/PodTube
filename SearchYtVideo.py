import CheckNewEpisodes

video_id = "8buCsouQEic"
response = CheckNewEpisodes.search_video(video_id)
#print(response)

CheckNewEpisodes.checkNewEpisodes(response, video_id)
