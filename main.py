import sys
import os
import wave
import AudioManipulation

def main():
    # File checking
    if len(sys.argv) != 2:
        print("Please provide WAV file name as a single argument!")
        return
    filename = sys.argv[1].strip()
    if not os.path.exists(filename):
        print(f"Could not locate {filename}.")
        return
    audio_file = wave.open(filename, "rb")
    # AudioProccessing.reverse("asdf.wav", audio_file)
    # AudioProccessing.derivative("derivative.wav", audio_file)
    # AudioProccessing.reverse()
    AudioManipulation.derivative("derivative.wav", audio_file)
    audio_file.close()

if __name__ == "__main__":
    main()
