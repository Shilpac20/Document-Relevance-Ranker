import os
from nltk.tokenize import word_tokenize
import math
from nltk.stem import PorterStemmer
import numpy as np
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
tf_idf_list={}
doc_size_list={}
def make_tf_idf_list(data,data_len,docid):
    doc_size_list[docid]=data_len
    for word in data:
        if word in tf_idf_list:
            if docid in tf_idf_list[word]:
                tf_idf_list[word][docid]+=1
            else:
                tf_idf_list[word][docid]=1
        else:
            tf_idf_list[word]={}
            tf_idf_list[word][docid]=1


def findbm25_score(n, f, qf, r, N, dl, avdl):
    K = k1 * ((1-b) + b * (float(dl)/float(avdl)) )
    first = math.log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2+1) * qf) / (k2 + qf)
    return first * second * third

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
#print(tf_idf_list)
avg_doc_len=0
for docid in doc_size_list.keys():
    avg_doc_len+=doc_size_list[docid]
#print(avg_doc_len)
avg_doc_len/=len(doc_size_list)
#print(avg_doc_len)
k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

path=current_path
os.chdir(path)
def clean_text(text):
    text=text.strip()
    exclude = set(string.punctuation)
    text= ''.join(ch if ch not in exclude else ' ' for ch in text)
    return text
query_path=input("enter the query text file name(with .txt extenstion) for BM25 Model results : ")
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
        #query_temp = word_tokenize(query)
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

        final_bm25_scores={}

        #print(avg_doc_len)
        for term in different_words:
            if term in tf_idf_list:
                #print(term)
                doc_dict = tf_idf_list[term]  # retrieve index entry
                #print(doc_dict)
                for docid, freq in doc_dict.items():  # for each document and its word frequency
                    score = findbm25_score(n=len(doc_dict), f=freq, qf=1, r=0, N=len(doc_size_list),
                                       dl=doc_size_list[docid], avdl=avg_doc_len)  # calculate score
                    if docid in final_bm25_scores:  # this document has already been scored once
                        final_bm25_scores[docid] += score
                    else:
                        final_bm25_scores[docid] = score
        query_scores = sorted(final_bm25_scores.items(), key=lambda x: x[1], reverse=True)
        #print(query_scores[1][1])
        doc_list=[]
        for docid,score in query_scores[:10]:
            doc_list.append(docid)
            with open('query_ans_BM25_model.txt', 'a+') as f:
                f.write(query_id + "," + "1" + "," + docid + ".txt," + "1" + "\n")
        #print(query_id," ",doc_list)
print("BM25 model finished")



