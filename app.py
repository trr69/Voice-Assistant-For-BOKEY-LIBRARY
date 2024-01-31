import json
import queue
import sounddevice as sd
import vosk
import ask_gpt
import time
import threading
import sys
import config


class Assistant:
    def __init__(self):
        self.q = queue.Queue()
        self.model = vosk.Model(config.PATH_MODEL)
        self.device = sd.default.device
        self.samplerate = int(sd.query_devices(self.device[0], 'input')['default_samplerate'])
        self.function_worked = False
        self.second = 10
        self.function_event = threading.Event()

    def wait_second(self):
        while self.second > 0:
            time.sleep(1)
            self.second -= 1
        self.second = 10

    def callback(self, indata, frames, time, status):
        if not self.function_event.is_set():
            self.q.put(bytes(indata))

    def recognize(self, data):
        trg = config.TRIGGERS.intersection(data.split())
        if trg or self.second != 10:
            self.function_event.set()
            ask_gpt.ask_gpt(prompt=data)
            print(data)
            my_thread = threading.Thread(target=self.wait_second)
            my_thread.start()
            self.function_event.clear()
            time.sleep(1)

    def start_assistant(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=16000, device=self.device[0], dtype='int16',
                               channels=1, callback=self.callback):
            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while True:
                try:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        data = json.loads(rec.Result())['text']
                        if data:
                            self.recognize(data)
                        print(data)

                    else:
                        print(f"Запись {rec.PartialResult()}")
                except KeyboardInterrupt:
                    print('Выход')
                    break
                except Exception as e:
                    print(f"error: {e}")
