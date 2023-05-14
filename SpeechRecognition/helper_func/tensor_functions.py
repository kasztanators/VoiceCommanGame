import numpy
import tensorflow as tf

seed = 42
tf.random.set_seed(seed)
numpy.random.seed(seed)

def get_spectrogram(waveform):
    input_len = 16000
    waveform = waveform[:input_len]
    zero_padding = tf.zeros(
        [16000] - tf.shape(waveform),
        dtype=tf.float32
    )
    waveform = tf.cast(waveform, dtype=tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = spectrogram[..., tf.newaxis]
    return spectrogram


def preprocess_audiobuffer(waveform):
    """
    waveform: ndarray of size (16000, )
    output: Spectogram Tensor of size: (1, `height`, `width`, `channels`)
    """
    #  normalize from [-32768, 32767] to [-1, 1]
    waveform = waveform / 32768
    waveform = tf.convert_to_tensor(waveform, dtype=tf.float32)
    spectogram = get_spectrogram(waveform)

    # add one dimension
    spectogram = tf.expand_dims(spectogram, 0)

    return spectogram