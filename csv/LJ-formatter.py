import re
import num2words
import unicodedata

lang = ''

print('\nObsługiwane języki: Polski')
lang_input = input('Jaki język jest używany w twoim audio wejściowym?: ')

if lang_input.strip().lower() == 'polski':
    lang = 'pl'

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

file = open('list.txt')

lineslist = []

# Utwórz obiekt pliku
file1 = open('list_corrected.txt', "w+")

# Czytaj wszystkie wiersze
lines = file.readlines()

# Przechodź przez wiersze jedna po drugiej
for line in lines:
    lineslist.append(line.strip())

# Zamknij plik
file1.close()

with open('transcript.csv', 'w+', encoding='utf-8') as f:
    for line in lineslist:
        decmark_reg = re.compile('(?<=\d),(?=\d)')

        comma_repl = decmark_reg.sub('',line.strip())

        normalized_sentence = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0)), lang=lang), str(comma_repl))
        final_line = f"{line.split('|')[0].replace('wavs/', '').replace('.wav', '').strip()}|{line.split('|')[1]}|{normalized_sentence.split('|')[1]}\n"
        
        final_line = strip_accents(final_line)

        f.write(final_line)
