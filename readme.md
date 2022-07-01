# Passthrough remote audio input
## Requirements
- pyaudio
- numpy
- pyyaml
- pynput

## Configuration
Check `config.yaml`  
- max_threashold: avoid cracking sound if the input volume is TOO loud
- output_device_name: Can be obtained by `get_devices.py`

## How the scripts work
Server: send sampled data via socket  
Client: listen server's socket and write the data to an output device. 
The output signal will be converted to microphone input source via either VB-Cable or Blackhole. Furthermore, by setting hotkey, you can temporary mute the sound on host.

## Audio output to input
- Windows: [VB-Cable](https://vb-audio.com/Cable/)
- macOS: [BlackHole](https://github.com/ExistentialAudio/BlackHole)

## TODO:
- [ ] noise reduction
