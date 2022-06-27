#!/usr/bin/env python

import pyaudio
import socket
import select
import numpy as np

class reduce_noise:
    # fuck u ignals and systems
    def __init__(self, chunk, dtype):
        self.chunk = chunk
        self.dtype = dtype
        # self.max_int = 2 ** (np.dtype(dtype).itemsize * 8 - 1) + 0.0
        # print(self.max_int)
        # self.j = np.complex(0, 1)
        # self.fir = np.zeros(chunk * 2)
        # self.fir[:(2 * chunk)] = 1.
        # self.fir /= self.fir.sum()
        #
        # self.fir_last = self.fir
        # self.avg_freq_buffer = np.zeros(chunk)
        # self.obj = - np.inf
        # self.t = 10
        #
        # # initialize sample buffer
        # self.buffer = np.zeros(chunk * 2)
    def run(self, string_audio_data):

        audio_data = np.fromstring(string_audio_data, dtype=self.dtype)
        print(audio_data)
        normalized_data = audio_data
        freq_data = np.fft.fft(normalized_data)
        psd = freq_data * np.conj(freq_data) / self.chunk
        mean = np.real(np.mean(psd))
        std = np.real(np.std(psd))
        threshold = mean - std
        print(mean, std)
        psd_idxs = psd > threshold  # array of 0 and 1
        psd_clean = psd * psd_idxs  # zero out all the unnecessary powers
        fhat_clean = psd_idxs * freq_data  # used to retrieve the signal
        audio_data = np.array(np.round_(np.real(np.fft.ifft(fhat_clean))), dtype=self.dtype)
        # write audio
        # audio_data = np.array(np.round_(synth[self.chunk:] * self.max_int), dtype=self.dtype)
        print(audio_data)
        print("-"*10)
        string_audio_data = audio_data.tostring()
        return string_audio_data



def mic_server(port=9487, format=pyaudio.paFloat32, formatnp=np.float32, channels=1, rate=48000, chunk=1024, max_threshold=0.5):
    print(f"Streaming port: {port}\nchannels: {channels}\nrate: {rate} Hz\nchunk: {chunk}")

    max_int = 2 ** (np.dtype(formatnp).itemsize * 8 - 1)

    audio = pyaudio.PyAudio()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('', port))
    serversocket.listen(5)

    rn = reduce_noise(chunk, formatnp)
    def reduceNoise(string_audio_data):
        ret = string_audio_data
        x = np.fromstring(string_audio_data, dtype=formatnp)
        mx = np.max(x)
        if (mx > max_threshold):
            x = x * max_threshold / mx
            ret = x.tostring()
        print(np.max(x))
        return ret
        # return rn.run(string_audio_data)
        # pass

    out_stream = audio.open(format=format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk)
    def callback(in_data, frame_count, time_info, status):
        to_send = reduceNoise(in_data)
        # out_stream.write(to_send)
        for s in read_list[1:]:
            s.send(to_send)
        return (None, pyaudio.paContinue)


    # start Recording
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk, stream_callback=callback)
    # stream.start_stream()

    read_list = [serversocket]
    print("recording...")
    try:
        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is serversocket:
                    (clientsocket, address) = serversocket.accept()
                    read_list.append(clientsocket)
                    print("Connection from", address)
                else:
                    try:
                        data = s.recv(2048)
                        if not data:
                            read_list.remove(s)
                    except ConnectionResetError:
                        read_list.remove(s)
                        pass
    except KeyboardInterrupt:
        pass


    print("finished recording")

    serversocket.close()
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == '__main__':
    mic_server(port=9487)