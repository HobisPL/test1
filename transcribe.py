# Importowanie bibliotek
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Utwórz obiekt rozpoznawania mowy
r = sr.Recognizer()


# Funkcja, która dzieli plik audio na fragmenty
# i stosuje rozpoznawanie mowy
def get_large_audio_transcription(path, lang):
    """
    Podział dużego pliku audio na fragmenty
    i zastosowanie rozpoznawania mowy dla każdego z tych fragmentów
    """
    # Otwórz plik audio za pomocą pydub
    sound = AudioSegment.from_wav(path)
    # Rozdzielaj dźwięk audio, w którym cisza trwa 700 milisekund lub dłużej i pobiera fragmenty
    chunks = split_on_silence(sound,
                              # Poeksperymentuj z tą wartością dla docelowego pliku audio
                              min_silence_len=500,
                              # Dostosuj to do wymagań
                              silence_thresh=sound.dBFS - 14,
                              # Zachowaj ciszę przez 1 sekundę, również z możliwością regulacji
                              keep_silence=500,
                              )
    folder_name = "fragmenty-audio"
    # Utwórz katalog do przechowywania fragmentów audio
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # Przetwarzaj każdy kawałek 
    for i, audio_chunk in enumerate(chunks, start=1):
        # Wyeksportuj fragment audio i zapisz go
        # w katalogu `folder_name`
        chunk_filename = os.path.join(folder_name, f"{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # Rozpoznaj fragment
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Spróbuj przekonwertować go na tekst
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                print("Błąd:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # Zwraca tekst dla wszystkich wykrytych fragmentów
    return whole_text
