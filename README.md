# Document-Relevance-Ranker
Please make sure the directory has read write permissions granted.

I assume that the python version is >=3.6. 
I am using nltk version 3.5.


To run the entire assignment please type the command make.

Please make sure english-corpora folder is present in the same directory as the python files and the Makefile.


The program will ask for the name of the file containing the list of queries. Please make sure that file is also in same directory as python files. Please provide the entire name of the query file for example query.txt



The entire assignment gets executed in 13-14mins approximately.


The answer of the IR systems is written in Qrel format in files namely query_ans_boolean_model.txt,query_ans_TF-IDF_model.txt,query_ans_BM25_model.txt.



The 20 queries and at least its top 10 relevant document(i have listed more in few cases) is given in query_list.txt file and Qrels.txt file respectively.



1.For Q1 tokenization and stemming , first i have preprocessed every file .The preprocessing included removal of extra white spaces, removing puntuation marks, ignoring non ascii characters. For tokenisation I have used word_tokenize of nltk. Once it has been tokenized , I remove all the stopwords and then do stemming. For stemming I have used Porter Stemmer of nltk. These stemmed words are then written to a new file with filename as docId_token_stem.txt i.e. if docId is C00001 then the preprocessed filename is C00001_token_stem.txt. 

These files are written in the english-corpora folder itself, so please ensure writing permissions are provided to that directory. To tokenize and stem and preprocess all the documents it takes around 11mins.



2.For Q2,  I have build the three IR models namely Boolean-model,Tf-idf Model and BM25 model.
In the 
Boolean-IR system , if the query has no connecting words like 'and','or','not' , I assume it means 'and' i.e. if a query is "Information Retrieval" , I assume it means "Information and Retrieval". 
I have implemented all the connecting word handling system i.e. my Boolean IR system can handle all 3 types of queries ('and','or','not').



In Tf-idf system I have used normalised Term frequency as the sizes of all documents are not same and there could be a extremely large size document having twice the count of a term than a small document, however the small document might be more relevant because it contains the term much more times if we scale the document sizes.



In BM25 model , I have implemeted the fuller version of BM25(as mentioned in sir's lecture). For the hyperparameters i had tested for different values and have used the values that provide me the optimal results(in terms of the queries i have used).




3.For q3, the 20 queries and their query id has been written in query_list.txt file and the qrels have been written in qrel_list.txt file. It is present inside 20111057-qrels.zip




5.The answer of the IR systems is written in Qrel format in files namely query_ans_boolean_model.txt,query_ans_TF-IDF_model.txt,query_ans_BM25_model.txt. Please make sure that the query file is present in same directory as the python files.
 Also please provide entire name of the query file for eg if its query.txt please mention it entirely (including .txt).Also in the query file the query_id and the free text should be tab separated. Please note that the query file name will be asked by each model,so please provide the query file name as and when it is asked to provide in the command line.
