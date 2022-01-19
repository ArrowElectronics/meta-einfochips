import speech_recognition as sr
import signal
import pyaudio
import time

import tensorflow as tf

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

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
    with tf.io.gfile.GFile(filename, 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def load_labels(filename):
    """Read in labels, one label per line."""
    return [line.rstrip() for line in tf.io.gfile.GFile(filename)]


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


def callback(recognizer, audio):

    run_graph(audio.get_wav_data())


def main():
    # initialized class for gracefully killed
    killer = GracefulKiller()

    # obtain audio from the microphone
    r = sr.Recognizer()

    available_microphone_list = sr.Microphone.list_microphone_names()
    print("Available Audio Devices : Index")

    for idx, val in enumerate(available_microphone_list):
        print(val, " : ", idx)

    while True:
        index = input("Which input (audio) device you want? Please provide index value (in number) : ")
        if index.isnumeric() and int(index) < len(available_microphone_list):
            print("You selected audio device : ", index)
            break
        else:
            print("Please provide correct Numeric value only")

    mic = sr.Microphone(device_index=int(index), sample_rate=RATE)

    # print("Noise cancellation ...")
    # with mic as source:
    #    r.adjust_for_ambient_noise(source, duration=1)

    # start listening in the background
    stop_listening = r.listen_in_background(mic, callback, phrase_time_limit=1)

    # `stop_listening` is now a function that, when called, stops background listening
    # stop_listening(wait_for_stop=False)

    print("Say Something Now!. It will continuously convert speech to text and Wait till user pressed CTRL+C ...\n")

    while killer.kill_now is False:
        time.sleep(1.0)

    print("Exiting Demo...")


if __name__ == '__main__':
    """Loads the model and labels """

    if not labels or not tf.io.gfile.exists(labels):
        tf.io.logging.fatal('Labels file does not exist %s', labels)

    if not graph or not tf.io.gfile.exists(graph):
        tf.io.logging.fatal('Graph file does not exist %s', graph)

    labels_list = load_labels(labels)

    # load graph, which is stored in the default session
    load_graph(graph)

    sess = tf.compat.v1.Session()

    # Input tensorflow layer
    softmax_tensor = sess.graph.get_tensor_by_name(output_name)

    main()
