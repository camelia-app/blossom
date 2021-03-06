# %%
import sys

sys.path.insert(0, "..")

import numpy as np
from blossom.equalizer import generate_equalizer
from sunflower.sunflower.song_loader import Song, load_from_disk
import sunflower.sunflower.song_analyzer as anlz
from sunflower.sunflower.song_analyzer import SongAnalyzer
from moviepy.editor import *
from moviepy.editor import concatenate_videoclips

%load_ext autoreload
%autoreload 2

# %%
# Loading example file

raw_audio, extension = load_from_disk("../assets/shazo_eq.wav")

song = Song(raw_audio, extension)

song.print_attributes()

# %%
# Analyze song

song_analyzer = SongAnalyzer(song, tempo=126)
# %%
lists = song_analyzer.process_decibel_per_frequencies(mode="peak")
# %%
size = (400, 400)

timestamps = lists[0]
length_step = timestamps[1] - timestamps[0]
list_bass = lists[1]
clips_detect = []

# %%
# Detect bass

for t in range(0, len(timestamps)):

    if list_bass[t] == 1:

        txt_clip = TextClip("bass_detected", fontsize=20, color="black")
        txt_clip = txt_clip.set_position((150, 150)).set_duration(length_step).set_start(timestamps[t])
        clips_detect.append(txt_clip)

# %%

clip = generate_equalizer(song, song_analyzer)

# %%
clip_final =CompositeVideoClip([clip]+clips_detect).set_duration(30)
clip_final.write_videofile(
    "../generated/equalizer.mp4",
    fps=24,
    temp_audiofile="../generated/temp-audio.m4a",
    remove_temp=True,
    codec="libx264",
    audio_codec="aac",
)

# %%

clip_final.write_gif("../generated/equalizer.gif", fps=24)
