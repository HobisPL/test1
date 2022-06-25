import re

from pydub import AudioSegment
from pydub.silence import split_on_silence

import glob
import os

import wave
import contextlib

import transcribe

skip_large_duration_files = True

file_number = 1

input_file = input('Wprowadź nazwę pliku wejściowego (dołącz rozszerzenie): ')

lang = ''

print('\nObsługiwane języki: Polski')
lang_input = input('Jaki język jest używany w twoim audio wejściowym?: ')

if lang_input.strip().lower() == 'polski':
    lang = 'pl'

# Przypisaj pliki
input_file = 'input/' + input_file

# Utwórz katalog jeśli nie istnieje
os.makedirs(os.path.dirname('input/'), exist_ok=True)
os.makedirs(os.path.dirname('output/'), exist_ok=True)
os.makedirs(os.path.dirname('output/wavs/'), exist_ok=True)

sound_file = AudioSegment.from_file(input_file)
sound_file = sound_file.set_frame_rate(22050)  # Nie zmieniaj tego
sound_file = sound_file.set_channels(1)  # Nie zmieniaj tego
audio_chunks = split_on_silence(sound_file, min_silence_len=250,  # 1000 tnie przy 1 sekundzie ciszy. 500 to 0,5 sek.
                                silence_thresh=-40)

for i, chunk in enumerate(audio_chunks):

    if not len(os.listdir('output/wavs')) == 0:
        list_of_files = glob.glob('output/wavs/*')  # * means all
        latest_file = max(list_of_files, key=os.path.getctime)

        # Wyciągnij liczby i zamień je na int
        list_of_nums = re.findall('\\d+', latest_file)

        if int(list_of_nums[0]) >= file_number:
            file_number = int(list_of_nums[0]) + 1

    out_file = "output/wavs/{0}.wav".format(file_number)
    print("Eksportowanie", out_file)

    chunk.export(out_file, format="wav")

    fname = out_file
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print('Długość:', duration)

    if skip_large_duration_files:
        if duration < 12:
            transcription = transcribe.get_large_audio_transcription(out_file, lang)

            if transcription != '':
                if os.path.isfile('output/list.txt'):
                    if os.stat("output/list.txt").st_size != 0:
                        with open('output/list.txt', 'a+') as f:
                            f.write(f'\nwavs/{file_number}.wav|' + transcription)
                            f.flush()
                    else:
                        with open('output/list.txt', 'a+') as f:
                            f.write(f'wavs/{file_number}.wav|' + transcription)
                            f.flush()
                else:
                    with open('output/list.txt', 'x') as f:
                        f.write(f'wavs/{file_number}.wav|' + transcription)

                file_number = file_number + 1
            else:
                os.remove(out_file)
        else:
            os.remove(out_file)

    else:
        transcription = transcribe.get_large_audio_transcription(out_file, lang)

        if transcription != '':
            if os.path.isfile('output/list.txt'):
                if os.stat("output/list.txt").st_size != 0:
                    with open('output/list.txt', 'a+') as f:
                        f.write(f'\nwavs/{file_number}.wav|' + transcription)
                        f.flush()
                else:
                    with open('output/list.txt', 'a+') as f:
                        f.write(f'wavs/{file_number}.wav|' + transcription)
                        f.flush()
            else:
                with open('output/list.txt', 'x') as f:
                    f.write(f'wavs/{file_number}.wav|' + transcription)

            file_number = file_number + 1
        else:
            os.remove(out_file)
