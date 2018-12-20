"""
Look at https://norvig.com/spell-correct.html
https://github.com/barrust/pyspellchecker
https://pyspellchecker.readthedocs.io/en/latest/

Working in mappy2. But might need to shift to python3
"""

from spellchecker import SpellChecker

spell = SpellChecker()
# spell = SpellChecker(distance=1)
# spell.word_frequency.load_text_file('./my_free_text_doc.txt')

# find those words that may be misspelled
#misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])
misspelled = spell.unknown(['number', 'of', 'military', 'personel', 'killed', 'in', 'training'])
for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))

    # Get a list of `likely` options
    print(spell.candidates(word))
misspelled = spell.unknown(['2006', 'form', '1040es'])
for word in misspelled:
    print(spell.correction(word))

#print spell.word_frequency.load_words(['microsoft', 'apple', 'google'])
#print spell.known(['microsoft', 'google'])

#print spell.correction('ogrnaized')
