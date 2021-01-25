# %%
# Loading example file

from equalizer import generate_equalizer
from sunflower.sunflower.song_loader import Song, load_from_disk
from sunflower.sunflower.song_analyzer import SongAnalyzer

# %%
# Loading example file

raw_audio, extension = load_from_disk("assets/shazo_eq.wav")

song = Song(raw_audio, extension)

song.print_attributes()

# %%
# Analyze song

song_analyzer = SongAnalyzer(song)

# %%

clip = generate_equalizer(song, song_analyzer)
clip.write_videofile(
    "generated/equalizer.mp4",
    fps=24,
    temp_audiofile="generated/temp-audio.m4a",
    remove_temp=True,
    codec="libx264",
    audio_codec="aac",
)

# %%

clip.write_gif("generated/equalizer.gif", fps=24)
