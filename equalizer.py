# %%
# Imports
import sys

# Accessing to my other git repos
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

from sunflower.sunflower.song_loader import Song, load_from_disk
from sunflower.sunflower.song_analyzer import SongAnalyzer
from sunflower.sunflower.utils import export_wav
from sunflower.sunflower.benchmark import run_benchmark
from sunflower.sunflower.song_visualizer import (
    visualize_waveform,
    visualize_waveform_plotly,
)
from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
import librosa
import soundfile as sf

# %%
# Loading example file

raw_audio, extension = load_from_disk("assets/shazo_eq.wav")

song = Song(raw_audio, extension)

song.print_attributes()

# %%
# Analyze song

song_analyzer = SongAnalyzer(song)

# %%


class AudioBar:
    def __init__(
        self,
        x,
        y,
        freq,
        decibel,
        color=(0, 0, 0),
        width=50,
        min_height=1,
        max_height=100,
        min_decibel=-80,
        max_decibel=0,
    ):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        decibel_height_ratio = abs(
            (max_height - min_height) / (max_decibel - min_decibel)
        )

        # TO DO : pool this value
        self.height = int(min(self.y - min_height, -decibel * decibel_height_ratio - 1))


def draw_rectangle(frame, audiobar):
    """Draw a rectangle in the frame."""

    # Change (top, bottom, left, right) to your coordinates
    left = int(audiobar.x)
    right = left + int(audiobar.width)
    bottom = audiobar.y
    top = audiobar.height

    frame[top:bottom, left:right] = audiobar.color

    return frame


# %%
# getting a matrix which contains amplitude values according to frequency and time indexes


def color_clip(size, duration, fps=25, color=(50, 50, 50)):
    return ColorClip(size, color, duration=duration)


frequencies = np.arange(50, 10000, 100)
size = (400, 400)
audioclip = AudioArrayClip(
    song.waveform.reshape(-1, 2),
    song.sr,
)

duration = audioclip.duration

fps_equalizer = 1 / 24
fps_equalizer = 1 / 24
time = 0
width = size[1] / len(frequencies)
y = size[0]
clips = []

comptdebug = 0


while len(clips) * fps_equalizer < duration:
    x = 0
    clip = color_clip(size, fps_equalizer)

    for c in frequencies:

        clip = clip.fl_image(
            lambda image: draw_rectangle(
                image,
                AudioBar(
                    x,
                    y,
                    c,
                    song_analyzer.get_decibel(time, c),
                    max_height=400,
                    width=width,
                ),
            )
        )

        x += width

    clip = clip.set_duration(fps_equalizer).set_start(time)
    clips.append(clip)

    time += fps_equalizer


clip = CompositeVideoClip(clips)
clip = clip.set_audio(audioclip)

# %%
clip.write_videofile(
    "generated/equalizer.mp4",
    fps=24,
    temp_audiofile="generated/temp-audio.m4a",
    remove_temp=True,
    codec="libx264",
    audio_codec="aac",
)
