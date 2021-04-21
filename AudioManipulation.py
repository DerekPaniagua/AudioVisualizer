import wave
import sys
import os.path
import random
import numpy


# -- Private Functions --
def _convert_bytes_to_frames(data_chunk, mono=False):
    rawdata = list(data_chunk)
    proccessed_data = []
    frames = []
    for i in range(0, len(rawdata), 2):
        proccessed_data.append(int.from_bytes(bytes(rawdata[i:i+2]),"little")) # Convert raw data into 16bit ints
    if mono:
        for val in proccessed_data:
            frames.append(AudioFrame(val))
    else: # Stereo
        for i in range(0, proccessed_data, 2):
            frames.append(AudioFrame(proccessed_data[i], proccessed_data[i+1]))
    return frames

def _convert_frames_to_bytes(frames, mono=False):
    data = []
    for frame in frames:
        if frame.mono != mono:
            raise Exception("Frame channel settings don't match provided settings!")
        data.append(frame.first_channel)
        if not mono:
            data.append(frame.second_channel)
    return bytes(data)

def _derive_samples(samples):
    pass

# -- Public Functions -- 
def generate_data_chunks(audio_file, chunk_size=100):
    audio_file.rewind()
    is_mono = True
    if audio_file.getnchannels() == 2:
        is_mono = False
    print(int(audio_file.getnframes() / chunk_size) )
    for i in range(0, int(audio_file.getnframes() / chunk_size)):
        data_chunk = audio_file.readframes(chunk_size)
        new_pos = audio_file.tell() + chunk_size
        if new_pos > audio_file.getnframes() - (chunk_size - 1):
            new_pos = audio_file.getnframes()
        audio_file.setpos(new_pos)
        yield _convert_bytes_to_frames(data_chunk, is_mono)

def derivative(filename, original_file):
    newfile = wave.open(filename, "wb")
    newfile.setparams(original_file.getparams())

    data = generate_data_chunks(original_file, chunk_size=128)
    chunk = next(data)
    print(len(chunk))
    print(chunk)
    # for data_chunk in generate_data_chunks(original_file):

def reverse(filename, original_file):
    newfile = wave.open(filename, "wb")
    newfile.setparams(original_file.getparams())
    data = list(original_file.readframes(original_file.getnframes()))
    proccessed_data = []
    for i in range(0, len(data), 4):
        proccessed_data.append(data[i:i+4])
    proccessed_data.reverse()
    data = []
    for frame in proccessed_data:
        data.extend(frame)
    newfile.writeframes(bytes(data))
    newfile.close()


# -- Classes --
class AudioFrame:
    def __init__(first, second=None):
        if not first:
            raise Exception("Must provide at least one channel value")         
        self.first_channel = left # Left/Mono
        self.second_channel = right # Right/None
        if second == None:
            self.mono = True
        else:
            self.mono = False