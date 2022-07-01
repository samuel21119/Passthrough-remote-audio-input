#!/usr/bin/env python

import pyaudio
import socket
import sys
import yaml
from time import sleep

import pyaudio

def mic_client(format=pyaudio.paFloat32, channels=1, rate=48000, chunk=1024, output_device_name="CABLE Input (VB-Audio Virtual C", ip="10.0.0.5",  port="9487"):
    # # ------- Start config -------
    # format = pyaudio.paFloat32
    # channels = 1
    # rate = 44100
    # chunk = 1024
    # output_device_name = "CABLE Input (VB-Audio Virtual C"
    # # ------- End config -------

    # output_device = int(sys.argv[3])
    output_device = None
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range(0, numdevices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
            if output_device_name == p.get_device_info_by_host_api_device_index(0, i).get('name'):
                output_device = i
                # print("Output Device id ", i, " - ", )

    devinfo = p.get_device_info_by_index(output_device)
    print("Selected device is ", devinfo.get('name'))
    p.terminate()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_source = (ip, int(port))
    s.connect(connect_source)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=rate, output=True, output_device_index=output_device, frames_per_buffer=chunk)

    try:
        while True:
            try:
                data = s.recv(chunk)
                s.send( bytes( "Client wave", "UTF-8" ) )
                stream.write(data)
            except socket.error:
                connected = False
                s = socket.socket()
                print("connection lost... reconnecting")
                while not connected:
                    # attempt to reconnect, otherwise sleep for 2 seconds
                    try:
                        s.connect(connect_source)
                        connected = True
                        print("re-connection successful")
                    except socket.error:
                        sleep(1)
    except KeyboardInterrupt:
        pass

    print('Shutting down')
    s.close()
    stream.close()
    audio.terminate()

if __name__ == '__main__':
    with open("config.yaml", "r") as config:
        d = yaml.safe_load(config)
        mic_client(port=d["port"], channels=d["channels"], rate=d["rate"], chunk=d["chunk"], output_device_name=d["output_device_name"], ip=d["ip"])
