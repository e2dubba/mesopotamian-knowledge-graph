# Scraping CDLI with Python

This post is about scraping CDLI, specifically the Lugalzagesi vase inscription. CDLI's composite texts are well formated and easy to grab. 

All this script initially does is pull a text, seperate the different signs used, and count them.   

## Importing 

We are going to use the following libraries. The only one that would need to be installed is `bs4`. BeautifulSoup is a library to manage HTML/XML. It is a really great tool for adding to `requests`.


```python
import requests
import re 
from collections import Counter

from bs4 import BeautifulSoup


req = requests.get('https://cdli.ucla.edu/tools/scores/Q001379.html')
```

## Extracting the Text from HTML, And Relevant Lines 

This particular text is a score transcription, where the first line of each section is an eclectic line drawn from the different peices of evidence. All of the particular peices of evidence are written out in full underneath the eclectic line. 


```python
soup = BeautifulSoup(req.text)
text = soup.get_text()
# Thankfully the cannonical lines start with Q[some Number] [lineNumber]: [Relevant text]
list_of_lines = re.findall(r'Q\d+ \d{3}:\n[^\n]*\n', text)
```

After we have the lines in a list, we also want to extract just the text


```python
list_of_lines = [x.split('\n')[1] for x in list_of_lines]
```

## Extracting the Individual Signs

After we have a list of lines, we want to take each sign spelled out in the transcription and put it into a single list. The Determinatives are put inside brackets `{}`, and need to be pulled out of the text


```python
DET_RE = re.compile(r'{([^}]*)}')
BRAC_TRANS = str.maketrans('', '', '[]{}')

def clean_punctuation(sign):
    '''For our purposes, we are not interested in the reconstructed signs, so we will 
    remove all of the brakets as well as clean up the determinative markings'''
    return sign.translate(BRAC_TRANS)
    

def extract_determinatives(sign):
    '''Extracting the determinatives after the line has been split by sign and word'''
    dete_match = DET_RE.search(sign)
    try:
        start = sign[:dete_match.start()]
        end = sign[dete_match.end():]
        sign = start+end 
        determinative = dete_match.group().replace('{', '').replace('}', '')
    except AttributeError:
        determinative = ''
    sign = clean_punctuation(sign)
    determinative = clean_punctuation(determinative)
    return sign, determinative
    
    
```

Now we can iterate over each of the lines, and create a single list of all of the signs. This first splits the text on both spaces and hyphens, and then addes all of the components of the sign to a snigle list


```python
list_of_signs = []

for line in list_of_lines:
    line = re.split(' |-', line)
    for sign in line:
        sign, deter = extract_determinatives(sign)
        if deter:
            list_of_signs.append(deter)      
        list_of_signs.append(sign)
```

With a single list we can count how often each sign occurs, with the module `Counter`. 


```python
counted = Counter(list_of_signs)
counted.most_common()
```




    [('ki', 22),
     ('d', 20),
     ('mu', 20),
     ('a', 19),
     ('e', 16),
     ('kur', 15),
     ('lugal', 14),
     ('na', 13),
     ('da', 11),
     ('en', 9),
     ('ga', 8),
     ('ma', 8),
     ('nam', 8),
     ('lil2', 7),
     ('ra', 7),
     ('utu', 7),
     ('ke4', 7),
     ('ni', 7),
     ('sze3', 7),
     ('si', 6),
     ('unu', 6),
     ('kalam', 6),
     ('an', 6),
     ('ge', 5),
     ('mah', 5),
     ('ne', 5),
     ('ba', 5),
     ('la', 5),
     ('dab6', 5),
     ('ha', 5),
     ('lu2', 4),
     ('igi', 4),
     ('u2', 4),
     ('sag', 4),
     ('u4', 4),
     ('ta', 4),
     ('ag2', 4),
     ('za3', 3),
     ('nisaba', 3),
     ('ensi2', 3),
     ('ka', 3),
     ('zi', 3),
     ('gal', 3),
     ('nin', 3),
     ('e3', 3),
     ('sa2', 3),
     ('szu', 3),
     ('zal', 3),
     ('gin7', 3),
     ('ti', 3),
     ('dumu', 2),
     ('U2', 2),
     ('umma', 2),
     ('szum2', 2),
     ('a2', 2),
     ('re', 2),
     ('giri3', 2),
     ('szu2', 2),
     ('gu2', 2),
     ('gar', 2),
     ('ab', 2),
     ('be2', 2),
     ('le', 2),
     ('sal', 2),
     ('nu2', 2),
     ('hul2', 2),
     ('bara2', 2),
     ('me', 2),
     ('tar', 2),
     ('gu4', 2),
     ('il2', 2),
     ('iri', 2),
     ('gi4', 2),
     ('he2', 2),
     ('sa6', 2),
     ('iszib', 1),
     ('bar', 1),
     ('gesztu2', 1),
     ('pa3', 1),
     ('sukkal', 1),
     ('suen', 1),
     ('szagina', 1),
     ('inanna', 1),
     ('tu', 1),
     ('gu7', 1),
     ('hur', 1),
     ('mes', 1),
     ('sanga', 1),
     ('girimx(|A.BU.HA.DU|)', 1),
     ('agrig', 1),
     ('dingir', 1),
     ('se3', 1),
     ('sig', 1),
     ('idigna', 1),
     ('buranun', 1),
     ('nim', 1),
     ('bi', 1),
     ('gaba', 1),
     ('nu', 1),
     ('tuku', 1),
     ('gi', 1),
     ('nun', 1),
     ('giri17', 1),
     ('uri5', 1),
     ('larsa', 1),
     ('szara2', 1),
     ('zabala5', 1),
     ('u8', 1),
     ('sila4', 1),
     ('gur5', 1),
     ('sig4', 1),
     ('|KI.AN|', 1),
     ('|KIN.KIN|', 1),
     ('nibru', 1),
     ('nidba', 1),
     ('su13', 1),
     ('de3', 1),
     ('du10', 1),
     ('de2', 1),
     ('tukumx(|SZU.TUR|)', 1),
     ('szita', 1),
     ('dah', 1),
     ('he', 1),
     ('u18', 1),
     ('szim', 1),
     ('dagal', 1),
     ('du11', 1),
     ('ubur', 1),
     ('du8', 1),
     ('esz2', 1),
     ('bala', 1),
     ('sipa', 1),
     ('gal2', 1),
     ('ri2', 1),
     ('ru', 1)]



## Conclusion 

This is just preliminary explorations of the sign lists in the Lugalsagezi inscription. This is just a preliminary to some more sophistiecated mthods that could be applied to the inscription. 
