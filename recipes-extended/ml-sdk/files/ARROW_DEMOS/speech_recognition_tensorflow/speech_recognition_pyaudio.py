import pyaudio
import wave
import audioop
import math
from collections import deque
import signal

import tensorflow as tf

THRESHOLD = 2000  # The threshold intensity that defines silence
# and noise signal (an int. lower than THRESHOLD is silence).

# FORMAT = pyaudio.paInt16
FORMAT = S16_LE
CHANNELS = 1
# RATE = 16000
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 1
WAVE_OUTPUT_FILENAME = 'recording.wav'

MIN_PROB = 0.20

labels = 'conv_labels.txt'
graph = 'speech_recognition_graph.pb'
input_name = 'wav_data:0'
output_name = 'labels_softmax:0'
show_no_of_label = 3


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def load_graph(filename):
    """Unpersists graph from file as default graph."""
    with tf.gfile.GFile(filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    """Read in labels, one label per line."""
    return [line.rstrip() for line in tf.gfile.GFile(filename)]


def run_graph(wav_data):
    """Runs the audio data through the graph and prints predictions."""

    add_linefeed = False

    # Feed the audio data as input to the graph.
    #   predictions  will contain a two-dimensional array, where one
    #   dimension represents the input image count, and the other has
    #   predictions per class

    predictions, = sess.run(softmax_tensor, {input_name: wav_data})

    # Sort to show labels in order of confidence
    top_k = predictions.argsort()[-show_no_of_label:][::-1]
    for node_id in top_k:
        human_string = labels_list[node_id]
        score = predictions[node_id]

        if score > MIN_PROB:
            print('%s (prediction score = %.2f)' % (human_string, score * 100))
            add_linefeed = True

    if add_linefeed:
        print("")

    return 0


def main():
    # initialized class for gracefully killed
    killer = GracefulKiller()

    audio = pyaudio.PyAudio()

    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    while True:
        index = input("Which input (audio) device you want? Please provide index value (in number) : ")
        if index.isnumeric() and int(index) < numdevices:
            print("You selected audio device : ", index)
            break
        else:
            print("Please provide correct Numeric value only")

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=int(index),
                        frames_per_buffer=CHUNK)

    while 1:
        # print("Speak Now...")

        frames = []
        slid_win = deque()

        # start Recording
        stream.start_stream()

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            sound_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(sound_data, 4))))
            frames.append(sound_data)

            # if user press ctrl + c then break from loop
            if killer.kill_now:
                break

        # stop Recording
        stream.stop_stream()

        if killer.kill_now:
            print("Exiting DEMO... ")

            stream.close()
            audio.terminate()
            break

        # print("********************")

        # silent = is_silent(frames)

        if sum([x > THRESHOLD for x in slid_win]) > 0:
            # data = pack('<' + ('h' * len(sound_data)), *sound_data)

            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            with open(WAVE_OUTPUT_FILENAME, 'rb') as wav_file:
                wav_data = wav_file.read()

                run_graph(wav_data)


if __name__ == '__main__':

    """Loads the model and labels """

    if not labels or not tf.gfile.Exists(labels):
        tf.logging.fatal('Labels file does not exist %s', labels)

    if not graph or not tf.gfile.Exists(graph):
        tf.logging.fatal('Graph file does not exist %s', graph)

    labels_list = load_labels(labels)

    # load graph, which is stored in the default session
    load_graph(graph)

    sess = tf.Session()

    # Input tensorflow layer
    softmax_tensor = sess.graph.get_tensor_by_name(output_name)

    main()
