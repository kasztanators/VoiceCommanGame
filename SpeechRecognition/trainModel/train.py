import pathlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from IPython import display
from helper import get_spectrogram
from exportModel import ExportModel
from plotter import display_plot_commands, plot_spectrogram, plot_waveform_grid, plot_waveform_and_spectrogram, \
    plot_spectrogram_grid, evaluate_model

DATASET_PATH = 'data/mini_speech_commands'
data_dir = pathlib.Path(DATASET_PATH)


def download_and_extract_dataset():
    if not data_dir.exists():
        tf.keras.utils.get_file(
            'mini_speech_commands.zip',
            origin="http://storage.googleapis.com/download.tensorflow.org/data/mini_speech_commands.zip",
            extract=True,
            cache_dir='.', cache_subdir='data')


def set_seed():
    seed = 42
    tf.random.set_seed(seed)
    np.random.seed(seed)


def get_commands():
    commands = np.array(tf.io.gfile.listdir(str(data_dir)))
    commands = commands[(commands != 'README.md') & (commands != '.DS_Store')]
    return commands


def squeeze(audio, labels):
    audio = tf.squeeze(audio, axis=-1)
    return audio, labels


def make_spec_ds(ds, label_names):
    return ds.map(
        map_func=lambda audio, label: (get_spectrogram(audio, label_names), label),
        num_parallel_calls=tf.data.AUTOTUNE)


def create_audio_datasets():
    train_ds, val_ds = tf.keras.utils.audio_dataset_from_directory(
        directory=data_dir,
        batch_size=64,
        validation_split=0.2,
        seed=0,
        output_sequence_length=16000,
        subset='both')
    return train_ds, val_ds


def get_model(input_shape, norm_layer, num_labels):
    return tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        # Downsample the input.
        tf.keras.layers.Resizing(32, 32),
        # Normalize.
        norm_layer,
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_labels),
    ])


def plot_command(command_name, file_dest, model, label_names):
    x = data_dir / file_dest
    x = tf.io.read_file(str(x))
    x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000, )
    x = tf.squeeze(x, axis=-1)
    x = get_spectrogram(x, label_names)
    x = x[tf.newaxis, ...]

    prediction = model(x)
    display_plot_commands(command_name, prediction)


def analyze_audio_example(example_audio, example_labels, label_names, sample_rate):
    for i in range(len(example_audio)):
        label = label_names[example_labels[i]]
        waveform = example_audio[i]
        spectrogram = get_spectrogram(waveform, label_names)

        print('Label:', label)
        print('Waveform shape:', waveform.shape)
        print('Spectrogram shape:', spectrogram.shape)
        print('Audio playback')
        display.display(display.Audio(waveform, rate=sample_rate))
    plot_waveform_and_spectrogram(waveform, spectrogram, label, sample_rate)
    return waveform


def compile_model(model):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )


def train_model(model, train_spectrogram_ds, val_spectrogram_ds):
    EPOCHS = 10
    history = model.fit(
        train_spectrogram_ds,
        validation_data=val_spectrogram_ds,
        epochs=EPOCHS,
        callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
    )
    return history


def run():
    # Set the seed value for experiment reproducibility.
    set_seed()
    # Uncomment TO DOWNLOAD DATASET AND DELETE 'no' directory manually
    #  download_and_extract_dataset()
    print(get_commands())
    train_ds, val_ds = create_audio_datasets()

    label_names = np.array(train_ds.class_names)
    print("label names:", label_names)

    train_ds = train_ds.map(squeeze, tf.data.AUTOTUNE)
    val_ds = val_ds.map(squeeze, tf.data.AUTOTUNE)

    test_ds = val_ds.shard(num_shards=2, index=0)
    val_ds = val_ds.shard(num_shards=2, index=1)

    for example_audio, example_labels in train_ds.take(1):
        print(example_audio.shape)
        print(example_labels.shape)

    plot_waveform_grid(example_audio, example_labels, label_names)

    waveform = analyze_audio_example(example_audio, example_labels, label_names, sample_rate=16000)

    train_spectrogram_ds = make_spec_ds(train_ds, label_names)
    val_spectrogram_ds = make_spec_ds(val_ds, label_names)
    test_spectrogram_ds = make_spec_ds(test_ds, label_names)

    example_spectrograms, example_spect_labels = next(iter(train_spectrogram_ds))

    plot_spectrogram_grid(example_spectrograms, example_spect_labels, label_names)

    train_spectrogram_ds = train_spectrogram_ds.cache().shuffle(10000).prefetch(tf.data.AUTOTUNE)
    val_spectrogram_ds = val_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)
    test_spectrogram_ds = test_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)

    input_shape = example_spectrograms.shape[1:]
    print('Input shape:', input_shape)
    num_labels = len(label_names)

    # Instantiate the `tf.keras.layers.Normalization` layer.
    norm_layer = tf.keras.layers.Normalization()
    # Fit the state of the layer to the spectrograms
    # with `Normalization.adapt`.
    norm_layer.adapt(data=train_spectrogram_ds.map(map_func=lambda spec, label: spec))

    model = get_model(input_shape, norm_layer, num_labels)

    model.summary()
    compile_model(model)
    history = train_model(model, train_spectrogram_ds, val_spectrogram_ds)
    metrics = history.history

    evaluate_model(model, test_spectrogram_ds, label_names, history, metrics)

    commands_to_plot = {
        'Yes': 'yes/0ab3b47d_nohash_0.wav',
        'Up': 'up/0ab3b47d_nohash_0.wav',
        'Stop': 'stop/0b40aa8e_nohash_0.wav',
        'Right': 'right/0ab3b47d_nohash_0.wav',
        'Left': 'left/0b09edd3_nohash_0.wav',
        'Go': 'go/0a9f9af7_nohash_0.wav',
        'Down': 'down/0a9f9af7_nohash_0.wav'
    }
    # Plotting goodness of fit of each command
    for command, filepath in commands_to_plot.items():
        plot_command(command, filepath, model, label_names)

    display.display(display.Audio(waveform, rate=16000))
    export_model = ExportModel(model, label_names)
    tf.keras.models.save_model(export_model.model, "../../code/saved_model/saved")


#   imported = tf.keras.models.load_model("../../code/saved_model/saved")


run()
