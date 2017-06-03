# No shebang here. You need to run it from the virtualenv.

import numpy
import python_speech_features.base
import scipy.io.wavfile
import subprocess

def remove_suffix(string, suffix):
    """Remove suffix from string if present, else do nothing."""
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string

def convert_mp3_to_wav(mp3_name, wav_name=None):
    """Use LAME to convert mp3 to wav on disk."""
    wav_name = wav_name or remove_suffix(mp3_name, ".mp3") + ".wav"
    # FIXME: Can we get lame to throw out stereo? The extra channel is
    # probably not worth our computation time.
    subprocess.run(["lame", "--decode", mp3_name, wav_name])
    return wav_name

def convert_wav_to_signal(wav_name):
    """Read a wav from disk and return a tuple (signal, sample_rate)."""
    return tuple(reversed(scipy.io.wavfile.read(wav_name)))

def convert_signal_to_mfccs(signal, sample_rate):
    return python_speech_features.base.mfcc(signal, samplerate=sample_rate)

