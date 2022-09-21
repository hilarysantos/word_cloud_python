
# Todas as instalações e importações necessárias para o script de nuvem de palavras e widget de upload

!pip install wordcloud
!pip install fileupload
!pip install ipywidgets
!jupyter nbextension install --py --user fileupload
!jupyter nbextension enable --py fileupload

import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import sys

# Esse é o uploader widget, para fazer o upload do arquivo de texto através de um botão de browser

def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 **10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)

_upload()

# Função que itera através das palavras em file_contents, remove a pontuação e conta a frequência de cada palavra. 
# A função ignora maiúsculas e minúsculas, palavras que não contêm todos os alfabetos e 
# palavras chatas como "e" ou "o". 
# Em seguida, será usada na função generate_from_frequencies para gerar a nuvem de palavras.

def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]
    
    # LEARNER CODE START HERE
    word_count = {}
    taken_text = []
    
    for word in file_contents.split():
        text = ""
        for letter in word.lower():
            if letter in uninteresting_words:
                pass
            elif letter not in uninteresting_words and letter.isalpha():
                text += letter
        
        if word not in uninteresting_words:
            taken_text.append(text)
    
    for word in taken_text:
        if word not in word_count:
            word_count[word] = 0
        word_count[word] += 1
    
    #wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(word_count)
    return cloud.to_array()

# Exiba a imagem da nuvem de palavras
  
myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation = 'nearest')
plt.axis('off')
plt.show()
