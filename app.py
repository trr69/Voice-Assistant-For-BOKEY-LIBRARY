import json
import queue
import sounddevice as sd
import vosk
import ask_gpt
import config
import time
import threading

q = queue.Queue()
model = vosk.Model(config.PATH_MODEL)
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
function_worked = False
second = 10
function_event = threading.Event()

def wait_second():
    global second
    while second > 0:
        time.sleep(1)
        second = second - 1
    second = 10

def callback(indata, frames, time, status):
    global function_event
    if not function_event.is_set():
        q.put(bytes(indata))


def recognize(data):
    trg = config.TRIGGERS.intersection(data.split())
    if trg or second != 10:
        function_event.set()
        ask_gpt.ask_gpt(prompt=data)
        print(data)
        my_thread = threading.Thread(target=wait_second)
        my_thread.start()
        function_event.clear()
        time.sleep(1)
    


def start_assistant():
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            try:
                data = q.get()
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.Result())['text']
                    if data:
                        recognize(data)
                    print(data)

                else:
                    print(rec.PartialResult())
            except KeyboardInterrupt:
                print('Выход')
                break
            except Exception as e:
                print(f"error: {e}")


