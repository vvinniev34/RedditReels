from pydub import AudioSegment
from datetime import date
# or
today = date.today().strftime("%Y-%m-%d")
path = f"RedditPosts/{today}/Texts" + "/AITAfortellingmywifethelockonm.mp3"
    
# export to mp3
sound = AudioSegment.from_file(path)
velocidad_X = 1.25 
so = sound.speedup(velocidad_X, 150, 25)
so.export(path[:-4] + '_Out.mp3', format = 'mp3')
