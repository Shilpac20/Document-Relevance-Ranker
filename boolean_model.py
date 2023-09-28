import os
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from nltk.corpus import stopwords
import math
import collections

# Folder Path
current_path=os.getcwd()
path = f"/english-corpora"

path=current_path+path
stemmer=PorterStemmer()
Stopwords = set(stopwords.words('english'))-set(["and","not","or"])

# Change the directory
os.chdir(path)
index_files = {}
vocab={}
def readfile(filepath,filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        data=f.read()
        #data=[word for word in data]
        data=data.split()
        #print(data)
        data_freq = freq_words(data)
        #print("hiiiii",data_freq)
        vocab.update(data_freq)
def freq_words(text):
        #unique_text = []
        freq_text = {}
        for word in text:
            if word in freq_text:
                freq_text[word]+=1
            else:
                freq_text[word]=1
            '''
            if word not in unique_text:
                unique_text.append(word)
                #print("hello ji",word)
        for word in unique_text:
            freq_text[word] = text.count(word)
            '''
        return freq_text
indx=1
for file in os.listdir():
    file_path = os.path.join(path,file)
    filename, file_extension = os.path.splitext(file_path)
    file_temp=filename.split("_token_")
    if(len(file_temp)>1):
        #head, tail = os.path.split(file_temp[0])
        #print(tail)
        #index_files[indx]=tail
        readfile(file_path,file_temp)
        indx+=1

unique_words=set(vocab.keys())
#print("hi",unique_words)

posting_list={}
indx=1
for file in os.listdir():
    file_path = os.path.join(path, file)
    filename, file_extension = os.path.splitext(file_path)
    file_temp = filename.split("_token_")
    #print(file_temp)
    if (len(file_temp) > 1):
    	head, tail = os.path.split(file_temp[0])
    	index_files[indx]=tail
    	file1 = open(file_path, "r")
    	data=file1.read()
    	data = data.split()
    	data_freq = freq_words(data)
    	for word in data_freq.keys():
    		if word in posting_list:
    			posting_list[word].append(indx)
    		else:
    			posting_list[word]=[indx]
    	indx = indx + 1

#path = "/IR_Assignments"
path=current_path
os.chdir(path)
def postfix_query(query):
        """ Parse Query
        Parsing done using Shunting Yard Algorithm
        """
        query.insert(0,'(')
        query.insert(len(query),')')
        #print(query)

        prec = {}
        prec['(']=0
        prec[')']=0
        prec['or'] = 1
        prec['and'] = 2
        prec['not'] = 3
        output = []
        operator_stack = []

        for token in query:

            if (token == '('):
                operator_stack.append(token)

                # if right bracket, pop all operators from operator stack onto output until we hit left bracket
            elif (token == ')'):
                operator = operator_stack.pop()
                while operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()

                    # if operator, pop operators from operator stack to queue if they are of higher precedence
            elif (token in prec):
                # if operator stack is not empty
                if (operator_stack):
                    current_operator = operator_stack[-1]
                    while (operator_stack and prec[current_operator] > prec[token]):
                        output.append(operator_stack.pop())
                        if (operator_stack):
                            current_operator = operator_stack[-1]
                operator_stack.append(token)  # add token to stack
            else:
                output.append(token.lower())

                # while there are still operators on the stack, pop them into the queue
        while (operator_stack):
                output.append(operator_stack.pop())

        return output

def and_op(left_list,right_list):
    return list(set(left_list).intersection(set(right_list)))
def or_op(left_list,right_list):
    return list(set(left_list).union(set(right_list)))
def not_op(right_list,total_doc_list):
    if(len(right_list)==0):
        return total_doc_list
    else:
        return list(set(total_doc_list)-set(right_list))
def clean_text(text):
        text = text.strip()
        exclude = set(string.punctuation)
        text = ''.join(ch if ch not in exclude else ' ' for ch in text)
        return text
#query
query_path=input("enter the query text file name(with .txt extenstion) for Boolean Model results : ")
with open(query_path,'r') as file:
    for line in file:
        fields = line.split('\t')
        query_id=fields[0]
        query=fields[1]
        #original_query=query
        #original_query=original_query.strip()
        #query = input('Enter your query:')
        query = clean_text(query)
        '''
        query=query.split()
        query_temp=[]
        for word in query:
            word = word.encode('ascii', 'ignore')
            word = word.decode('UTF-8')
            query_temp.append(word)
        query=' '.join(word for word in query_temp)
        '''
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
        query_with_connections=[]
        flag=0
        for word in query:
            if len(query_with_connections)==0 or word=='and' or word=='or' or query_with_connections[-1]=='and' or query_with_connections[-1]=='or' or query_with_connections[-1]=='not':
                query_with_connections.append(word)

            else:
                query_with_connections.append('and')
                query_with_connections.append(word)

        query_post=postfix_query(query_with_connections)

        #print(query_id," ",query_post," ",query_with_connections)
        query_post=collections.deque(query_post)
        results_stack = []
        total_files = list(range(1, len(index_files) + 1))
        while query_post:
            token = query_post.popleft()
            result = []  # the evaluated result at each stage
            # if operand, add postings list for term to results stack
            if (token != 'and' and token != 'or' and token != 'not'):
                # default empty list if not in dictionary
                if (token in posting_list):
                    result = posting_list[token]
            elif (token == 'and'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result = and_op(left_operand, right_operand)  # evaluate AND

            elif (token == 'or'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result =or_op(left_operand, right_operand)  # evaluate OR

            elif (token == 'not'):
                right_operand = results_stack.pop()

                result = not_op(right_operand, total_files)  # evaluate NOT

            results_stack.append(result)

            # NOTE: at this point results_stack should only have one item and it is the final result
        if len(results_stack) != 1:
            doc_list=[]
            for i in range(1,11,1):
                doc_list.append(index_files[i])

                with open('query_ans_boolean_model.txt', 'a+') as f:
                    f.write(query_id+","+"1"+","+index_files[i]+".txt,"+"0"+"\n")
            #print(query_id," ",doc_list)  # check for errors

        else:
            query_result=results_stack.pop()
            #query_result=sorted(query_result)
            final_ans=[]
            for i in query_result:
                final_ans.append(index_files[i])
            doc_list = []
            #final_ans=sorted(final_ans)
            for i in final_ans[:10]:
                doc_list.append(i)
            for doc in doc_list:
                with open('query_ans_boolean_model.txt', 'a+') as f:
                    f.write(query_id + "," + "1" + "," + doc + ".txt," + "1" + "\n")
            if(len(doc_list)<10):
                for i in range(1,len(index_files)):
                    if(len(doc_list)==10):
                        break
                    if index_files[i] not in doc_list:
                        doc_list.append(index_files[i])
                        with open('query_ans_boolean_model.txt', 'a+') as f:
                            f.write(query_id + "," + "1" + "," + index_files[i] + ".txt," + "0" + "\n")
            #print(query_id," ",doc_list)
print("Boolean IR model Finished")


