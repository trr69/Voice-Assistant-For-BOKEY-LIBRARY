import os
from typing import Any
import torch
from decorators import check_time_decorator
import wave
import pyaudio

class TTSModel:
    def __init__(self, model_path='models/model.pt', sample_rate=48000):
        self.device = torch.device('cpu')
        torch.set_num_threads(4)
        self.model_path = model_path
        self.sample_rate = sample_rate

        if not os.path.isfile(self.model_path):
            self.download_model()
        self.load_model()

    @check_time_decorator
    def __call__(self, text:str, *args: Any, **kwds: Any) -> Any:
        path_to_waw = self.model.save_wav(text=text, sample_rate=self.sample_rate)
        self.play_wav_file(path_to_waw)
        self.delete_file(path_to_waw)

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Ошибка удаления файла {file_path}: {e}")

    def download_model(self):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt', self.model_path)

    def play_wav_file(self, file_path):
        chunk = 1024
        wf = wave.open(file_path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def load_model(self):
        try:
            package_importer = torch.package.PackageImporter(self.model_path)
            self.model = package_importer.load_pickle("tts_models", "model")
            self.model.to(self.device)
        except FileNotFoundError:
            print('В директории models нет файла model.py')
        

    

