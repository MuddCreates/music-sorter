# No shebang here. You need to run it from the virtualenv.

import numpy
import python_speech_features.base
import scipy.cluster.vq
import scipy.io.wavfile
import subprocess
import sys

def remove_suffix(string, suffix):
    """Remove suffix from string if present, else do nothing."""
    if string.endswith(suffix):
        return string[:-len(suffix)]
    return string

def convert_mp3_to_wav(mp3_name, wav_name=None):
    """Use LAME to convert mp3 to wav on disk."""
    wav_name = wav_name or remove_suffix(mp3_name, ".mp3") + ".wav"
    # FIXME: Should lame throw out stereo? What about decreasing
    # bitrate?
    subprocess.run(["lame", "--decode", mp3_name, wav_name])
    return wav_name

def convert_wav_to_signal(wav_name):
    """Read a wav from disk and return a tuple (signal, sample_rate).

    The length of signal divided by sample_rate will be the length of
    the wav in seconds.
    """
    return tuple(reversed(scipy.io.wavfile.read(wav_name)))

def convert_signal_to_mfcc_frames(signal,
                                  sample_rate,
                                  frame_size=25.6/1000,
                                  frame_step=10/1000):
    """Convert a signal into frames and report the MFCCs for each.

    The number of MFCC frames multiplied by frame_step will be the
    length of the wav, unless it's stereo (in which case it will be
    twice the length of the wav, see [1]). Each MFCC frame is a vector
    of length 13, the number of MFCC coefficients.

    [1]: https://github.com/jameslyons/python_speech_features/issues/42
    """
    return python_speech_features.base.mfcc(signal, samplerate=sample_rate)

class Cluster:
    """A cluster of MFCC frames. Only the summary statistics are preserved."""
    def __init__(self, frames=None, mean=None, covariance=None, weight=None):
        """Create a Cluster from a numpy array of MFCC frames.

        Alternatively, pass mean, covariance, and weight instead of frames."""
        if frames is not None:
            # TODO: calculate mean and covariance -- but how on earth
            # do you get scalars for the mean and covariance of a set
            # of points??
            self.mean = None
            self.covariance = None
            self.weight = len(frames)
        else:
            self.mean = mean
            self.covariance = covariance
            self.weight = weight
    def distance(self, other):
        return (self.covariance / other.covariance +
                other.covariance / self.covariance +
                (self.mean - other.mean) ** 2 *
                (1 / self.covariance + 1 / other.covariance))
    def __repr__(self):
        return ("Cluster(mean={}, covariance={}, weight={})"
                .format(self.mean, self.covariance, self.weight))

class Signature:
    """The signature for a song, used for computing distances between songs."""
    def __init__(self, frame_groups=None, clusters=None):
        """Create a Signature from a list of MFCC frame groups.

        Alternatively, pass a list of Cluster objects."""
        if frame_groups is not None:
            self.clusters = [Cluster(frame_group) for frame_group in frame_groups]
        else:
            self.clusters = clusters
    def __repr__(self):
        return "Signature(clusters=[{}])".format(", ".join(map(repr, self.clusters)))

def cluster_mfcc_frames(frames, num_clusters=16):
    """Cluster MFCC frames using k-means and return a list of the groups."""
    normalized_frames = scipy.cluster.vq.whiten(frames)
    means, overall_distortion = scipy.cluster.vq.kmeans(
        normalized_frames, num_clusters)
    cluster_indices, distortions = scipy.cluster.vq.vq(normalized_frames, means)
    frame_groups = [[] for i in range(num_clusters)]
    for frame, cluster_index in zip(frames, cluster_indices):
        frame_groups[cluster_index].append(frame)
    return frame_groups

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename.endswith(".mp3"):
            print("Converting wav to mp3.")
            wav_name = convert_mp3_to_wav(filename)
        elif filename.endswith(".wav"):
            wav_name = filename
        else:
            print("usage: main.py [FILENAME.mp3 | FILENAME.wav]")
            sys.exit(1)
        print("Converting wav to signal.")
        signal, sample_rate = convert_wav_to_signal(wav_name)
        print("Converting signal to MFCC frames.")
        frames = convert_signal_to_mfcc_frames(signal, sample_rate)
        print("Clustering MFCC frames.")
        frame_groups = cluster_mfcc_frames(frames)
        print("Computing signature.")
        signature = Signature(frame_groups)
