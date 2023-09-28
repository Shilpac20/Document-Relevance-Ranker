import os
from nltk.tokenize import word_tokenize
import math
from nltk.stem import PorterStemmer
import numpy as np
from numpy import dot
from numpy.linalg import norm
import string
from nltk.corpus import stopwords


# Folder Path
current_path=os.getcwd()
path = f"/english-corpora"

path=current_path+path
stemmer=PorterStemmer()
Stopwords = set(stopwords.words('english'))

# Change the directory
os.chdir(path)

np.seterr(divide='ignore', invalid='ignore')
tf_doc={}
idf_doc={}

def make_tf_idf_list(data,data_len,docid):
    word_count_list = {}
    for word in data:
        if word in word_count_list:
            word_count_list[word] += 1
        else:
            word_count_list[word] = 1

    for word in word_count_list.keys():
        if word in tf_doc.keys():
            tf_doc[word][docid]=word_count_list[word]/float(data_len)
        else:
            tf_doc[word]={}
            tf_doc[word][docid]=word_count_list[word]/float(data_len)
        if word in idf_doc:
            idf_doc[word]+=1
        else:
            idf_doc[word]=1
def make_tf_idf_query(query):
    tf_query={}
    idf_query={}
    word_list={}
    for word in query:
        if word in word_list:
            word_list[word]+=1
        else:
            word_list[word]=1
    for word in word_list.keys():
        tf_query[word]=word_list[word]
        if word in idf_doc:
            idf_query[word]=idf_doc[word]
        else:
            #print(word)
            idf_query[word]=0

    return tf_query,idf_query
count=0
final_scores={}
for file in os.listdir():
    file_path = os.path.join(path, file)
    filename, file_extension = os.path.splitext(file_path)
    file_temp = filename.split("_token_")
    #print(file_temp)
    if (len(file_temp) > 1):
        head, tail = os.path.split(file_temp[0])
        id=tail
        file = open(file_path, "r")
        data = file.read()
        data = data.split()
        make_tf_idf_list(data,len(data),id)
        count+=1
        final_scores[id]=[]

path=current_path
os.chdir(path)
for words in idf_doc.keys():
    idf_doc[words]=math.log(float(count) / idf_doc[words])
def clean_text(text):
    text=text.strip()
    exclude = set(string.punctuation)
    text= ''.join(ch if ch not in exclude else ' ' for ch in text)
    return text
def compute_cosine_sim_score(query,tf_query,idf_query,docid):
    dot_product = 0
    qry_mod = 0
    doc_mod = 0
    tf_idf_query={}
    tf_idf_doc={}
    for word in query:
        tf_idf_query[word]=tf_query[word]*idf_query[word]
        tf_idf_doc[word]=0
        if word in tf_doc:
            doc_list=tf_doc[word].keys()
            if docid in doc_list:
                tf_idf_doc[word]=tf_doc[word][docid]*idf_doc[word]
        dot_product += tf_idf_query[word] * tf_idf_doc[word]
        # ||Query||
        qry_mod += tf_idf_query[word] * tf_idf_query[word]
        # ||Document||
        doc_mod += tf_idf_doc[word] * tf_idf_doc[word]
    qry_mod = np.sqrt(qry_mod)
    doc_mod = np.sqrt(doc_mod)
    # implement formula
    denominator = qry_mod * doc_mod
    cos_sim = dot_product / denominator
    if math.isnan(cos_sim):
        cos_sim=0.0
    return cos_sim
query_path=input("enter the query text file name(with .txt extenstion) for Tf-Idf Model results : ")
with open(query_path,'r') as file:
    for line in file:
        fields = line.split('\t')
        query_id=fields[0]
        query=fields[1]
        original_query = query
        original_query=original_query.strip()
        query = clean_text(query)
        query = query.encode('ascii', 'ignore')
        query = query.decode('UTF-8')
        query = word_tokenize(query)
        # data=''.join(data)
        # data=word_tokenize(data)
        query = [word.lower() for word in query]
        query_temp = [word for word in query if word not in Stopwords]
        query=[]
        for words in query_temp:
            query.append(stemmer.stem(words))
        connecting_words = []
        different_words = []
        for word in query:
            if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
                different_words.append(word.lower())
            else:
                connecting_words.append(word.lower())

        tf_query,idf_query=make_tf_idf_query(different_words)
        for docid in final_scores.keys():
            final_scores[docid]=compute_cosine_sim_score(different_words,tf_query,idf_query,docid)

        query_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        doc_list = []
        for docid, score in query_scores[:10]:
            doc_list.append(docid)
            with open('query_ans_TF-IDF_model.txt', 'a+') as f:
                f.write(query_id + "," + "1" + "," + docid + ".txt," + "1" + "\n")
        #print(query_id, " ", doc_list)
print("TF-IDF Model finished")




