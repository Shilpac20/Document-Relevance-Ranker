# Import Module
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import os
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords



# Folder Path
current_path=os.getcwd()
path = f"/english-corpora"
#print(current_path," ",path)
path=current_path+path
#print(path)
# Change the directory
os.chdir(path)

#tokenizer=WhitespaceTokenizer()
stemmer=PorterStemmer()
Stopwords = set(stopwords.words('english'))

# Read text File
def read_text_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as f:
        data=f.read()
        data=clean_text(data)
        data=data.split()
        data_temp=[]
        for word in data:
            word = word.encode('ascii', 'ignore')
            word = word.decode('UTF-8')
            data_temp.append(word)
        data=' '.join(word for word in data_temp)
        data=word_tokenize(data)
        #data=''.join(data)
        #data=word_tokenize(data)
        data = [word.lower() for word in data]
        data = [word for word in data if word not in Stopwords]
        data_stemed=[]
        for words in data:
            data_stemed.append(stemmer.stem(words))
        data = ' '.join(data_stemed)


        filename, file_extension = os.path.splitext(file_path)
        with open(filename+"_token_stem"+file_extension,'w+') as f:
            f.write(data)
        #print(f.read())

#clean the data
def clean_text(text):
    text=text.strip()
    exclude = set(string.punctuation)
    text= ''.join(ch if ch not in exclude else ' ' for ch in text)
    return text
# iterate through all file

for file in os.listdir():
    # Check whether file is in text format or no
    file_path = os.path.join(path,file)
    #print(file," ",file_path)
    '''
    filename, file_extension = os.path.splitext(file_path)
    if(file_extension=='.txt'):
        i+=1
    '''
    # call read text file function
    read_text_file(file_path)
print("Finished Tokenisation and Stemming")



