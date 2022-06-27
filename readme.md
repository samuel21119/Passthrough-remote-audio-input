# Passthrough remote audio input
## Requirements
- pyaudio
- numpy

## Configuration
### Server
- format
- channels
- rate
- chunk
### Client
- format
- channels
- rate
- chunk
- output_device_name: Can be obtained by `get_devices.py`

## How the scripts work
Server: send sampled data via socket  
Client: listen server's socket and output the data to an output device. 
The output signal will be converted to microphone input source via either VB-Cable or Blackhole.

## Audio output to input
- Windows: [VB-Cable](https://vb-audio.com/Cable/)
- macOS: [BlackHole](https://github.com/ExistentialAudio/BlackHole)

## TODO:
- [ ] noise reduction
