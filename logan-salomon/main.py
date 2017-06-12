#!/usr/bin/env python

import numpy
import pyemd
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
    def __init__(self, frames):
        """Create a Cluster from a list of MFCC frames."""
        frames = numpy.array(frames)
        self.mean = frames.mean(axis=0)
        self.covariance = numpy.cov(frames.T)
        self.weight = len(frames)
    def distance(self, other):
        # Implementation of symmetric Kullback-Leibler distance
        # between two multivariate normal distributions, see [1].
        #
        # The asymmetric Kullback-Leibler distance is defined as:
        #
        #   1/2 ( tr( inv(cov_2) * cov_1 ) +
        #         ( transpose( mean_2 - mean_1 ) *
        #           inv( cov_2 ) *
        #           ( mean_2 - mean_1 ) ) -
        #         dimension +
        #         ln ( det( cov_2 ) / det ( cov_1 ) ) )
        #
        # We compute the symmetric distance as:
        #
        #   D_sym(N1, N2) = D_asym(N1, N2) + D_asym(N2, N1)
        #
        # This causes the ln term to drop out.
        #
        # Note that the inverse of the covariance matrix is called the
        # precision matrix.
        #
        # [1]: https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence#Kullback.E2.80.93Leibler_divergence_for_multivariate_normal_distributions
        dimension = len(self.mean)
        difference = other.mean - self.mean
        covariance1 = self.covariance
        covariance2 = other.covariance
        # FIXME: sometimes these matrices are singular!
        precision1 = numpy.linalg.inv(covariance1)
        precision2 = numpy.linalg.inv(covariance2)
        return 1/2 * (
            precision2.dot(covariance1).trace() +
            precision1.dot(covariance2).trace() +
            difference.T.dot(precision1 + precision2).dot(difference)
        ) - dimension
    def __repr__(self):
        return ("<Cluster mean={} covariance={} weight={}>"
                .format(self.mean, self.covariance, self.weight))

class Signature:
    """The signature for a song, used for computing distances between songs."""
    def __init__(self, frame_groups):
        """Create a Signature from a list of MFCC frame groups."""
        self.clusters = [Cluster(frame_group) for frame_group in frame_groups]
    def distance(self, other):
        num_clusters = len(self.clusters)
        dist_matrix = numpy.empty([num_clusters, num_clusters])
        for i in range(num_clusters):
            for j in range(num_clusters):
                dist = self.clusters[i].distance(self.clusters[j])
                dist_matrix[i, j] = dist_matrix[j, i] = dist
        signature1 = numpy.array(c.weight for cluster in self.clusters)
        signature2 = numpy.array(c.weight for cluster in other.clusters)
        return pyemd.emd(signature1, signature2, dist_matrix)
    def __repr__(self):
        return "<Signature {}>".format(" ".join(map(repr, self.clusters)))

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
        filenames = sys.argv[1:]
        signatures = {}
        for filename in filenames:
            print("Processing '{}'.".format(filename))
            if filename.endswith(".mp3"):
                print("  Converting wav to mp3.")
                wav_name = convert_mp3_to_wav(filename)
            elif filename.endswith(".wav"):
                wav_name = filename
            else:
                print("usage: main.py [FILENAME.mp3 | FILENAME.wav]")
                sys.exit(1)
            print("  Converting wav to signal.")
            signal, sample_rate = convert_wav_to_signal(wav_name)
            print("  Converting signal to MFCC frames.")
            frames = convert_signal_to_mfcc_frames(signal, sample_rate)
            print("  Clustering MFCC frames.")
            frame_groups = cluster_mfcc_frames(frames)
            print("  Computing signature.")
            signature = Signature(frame_groups)
            signatures[filename] = signature
        for filename1, signature1 in signatures.items():
            for filename2, signature2 in signatures.items():
                if filename1 != filename2:
                    print("Comparing '{}' with '{}'."
                          .format(filename1, filename2))
                    distance = signature1.distance(signature2)
                    print("  Distance: {}".format(distance))
