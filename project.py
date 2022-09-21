#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import unicode_literals
from hazm import *
from hazm import stopwords_list
import os
import string
import re
import math







# In[ ]:


docs = []
AllWords = []
PositionIndexArray = []
AllBigrams = []
with open("PersianPoemsData/Stopwords/Stopwords" , 'r', encoding="utf-8") as f:
    stops = []
    for line in f:
        line = line[:-1]
        stops.append(line)
f.close()
with open('wordss.txt', 'r', encoding="utf-8") as f:
    for line in f:
        line = line[:-1]
        if line != '***':
            AllWords.append(line)
f.close()


# # class for each documents

# In[ ]:


class Doc:
    def __init__(self,lines,id,main):
        self.lines = lines
        self.id = id
        self.main = main


# # class for Positional Index

# In[ ]:


class PosInd:
    def __init__(self,word,abundance,docPositions):
        self.word = word
        self.abundance = abundance
        self.docPositions = docPositions


# In[ ]:


def Bigram(text):
    bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    return bigrams


# # Prepare data

# In[ ]:


def prepareData(lines,name = ''):
    normalizer = Normalizer()
    stemmer = Stemmer()
    res = []
    normalizeLine = []
    tokensWithStop = []
    tokensLine = []
    stemsLine = []
    for line in lines:
        lines22 = word_tokenize(line)
        line2 = []
        for w in lines22:
            if w not in stops:
                w = normalizer.normalize(w)
                w = stemmer.stem(w)
                line2.append(w)
        res.append(line2)
    doc = Doc(lines,name,res)
    return doc


# # Method for add document

# In[ ]:


def addDoc(name):
    ch = True
    for doc in docs:
        if doc.id == name:
            ch = False
            break
    if ch:
        try:
            lines = []
            with open("PersianPoemsData/Poems/"+str(name)+".persian_poem" , 'r', encoding="utf-8") as f:
                for line in f:
                    line = line[:-1]
                    lines.append(line)
            f.close()
            lines2 = []
            for line in lines:
                if "\u200c" in line:
                    line = line.replace("\u200c"," ")
                lines2.append(line)
            lines = lines2
            AllBigrams.append([name,Bigram(lines)])
            docs.append(prepareData(lines,name))
        except:
            a = 5
    else:
        print('this doc has been added!!')


# # Method for remove doc

# In[ ]:


def removedoc(name):
    index = -1
    for doc in docs:
        if doc.id == name:
            index = docs.index(doc)
            break
    if index > -1 :
        docs.remove(index)
    else:
        print('this doc does not exist')


# # Method for read all files

# In[ ]:


def readAllDocs():
    i = 2624
    maxi = 31465
    while i < maxi:
        addDoc(i)
        i+=1


# # Method for add word to posisional index

# In[ ]:


def addWordToWords(word):
    normalizer = Normalizer()
    stemmer = Stemmer()
    word = normalizer.normalize(word)
    word = stemmer.stem(word)
    check = True
    for wo in PositionIndexArray:
        if wo.word == word:
            check = False
            break
    if check:
        bad_chars = [';', ':', '!', '*','(',')','[',']','{','}',',','@','-']
        for i in bad_chars :
            word = word.replace(i, '') 
        count = 0
        docposes=[]
        for doc in docs:
            countInDoc = 0
            positions = []
            checkInDoc = False
            for line in doc.lines:
                if word in line:
                    checkInDoc = True
                    countInDoc +=1
                    a = [m.start() for m in re.finditer(word, line)]
                    aac = len(a)
                    b = doc.lines.index(line)
                    positions.append([b,a])
            if checkInDoc :
                count += aac
                id = doc.id
                docpos = [id,countInDoc,positions]
                docposes.append(docpos)
        posInd = PosInd(word,count,docposes)
        PositionIndexArray.append(posInd)


# # Step 1

# In[ ]:


n = input('enter a number for lines : ')
lines = []
for i in range(int(n)):
    line = input('Enter a line : ')
    lines.append(line)
doc = prepareData(lines)
print('doc.lines')
print(doc.lines)
print('doc.prepares')
print(doc.main)
print('doc.id')
print(doc.id)

# enter a number for lines 5
# Enter a line رفتم و برگشتم دیدم
# Enter a line هیچ کسی نبود و پرسیدم
# Enter a line کسی هست که بدهد جوابها را
# Enter a line گفتند بستگی دارد چ باشد پرسشا
# Enter a line ناگهان دیدمان


# In[ ]:


# PositionIndexArray[0].word


# # Step 2

# ## 2-1  create index from all docs
# ### 2-1-1 posision index
# #### 2-1-1-1 read all documents :

# In[ ]:


readAllDocs()


# #### 2-1-1-2   add all word that we read from docs to posision index :

# In[ ]:


for word in AllWords:
    addWordToWords(word)


# ## 2-2   add a document with name :

# In[ ]:


a = input('Enter name of doc (like 2625) : ')
addDoc(int(a))


# ## 2-3   remove a document with name :

# In[ ]:


a = input('Enter name of doc (like 2625) : ')
removedoc(int(a))


# ## 2-4   add to file :

# In[ ]:


with open('sz.sz', 'w' , encoding="utf-8") as f:
    for i in PositionIndexArray:
        f.write(i.word+','+str(i.abundance)+',{\n')
        for doc in i.docPositions:
            f.write(str(doc[0])+','+str(doc[1])+',[')
            for pos in doc[2]:
                f.write(str(pos[0])+'-<')
                for posLine in pos[1]:
                    if(pos[1].index(posLine) == len(pos[1]) - 1):
                        f.write(str(posLine))
                    else:
                        f.write(str(posLine)+'@')
                if(doc[2].index(pos) == len(doc[2]) - 1):
                    f.write('>')
                else:
                    f.write('>!')
            f.write(']\n')
        f.write('}\n***\n')
f.close()


# ## 2-5   read from file :

# In[ ]:


listOfLines = []
with open('sz.sz', 'r' , encoding="utf-8") as f:
    for line in f:
        line = line[:-1]
        listOfLines.append(line)
f.close()
i = 0
list2 = []
listAll = []
for line in listOfLines:
    if(line == '***'):
        i = 0
    else:
        i+=1
        list2.append(line)
    if i == 0:
        list2 = list2[:-1]
        listAllOneDoc = []
        for l in list2:
            if list2.index(l) == 0:
                l2 = l.split(',')
                listAllOneDoc.append(l2[0])
                listAllOneDoc.append(int(l2[1]))
            else:
                l2 = l.split(',')
                list5 = []
                for ll in l2:
                    if l2.index(ll) == 0:
                        list5.append(int(ll))
                    elif l2.index(ll) == 1:
                        list5.append(int(ll))
                    else:
                        l3 = ll[1:-1]
                        l3 = l3.split('!')
                        list6 = []
                        for l4 in l3:
                            l5 = l4.split('-')
                            list7 = []
                            list8 = []
                            for l6 in l5:
                                if l5.index(l6) == 0 :
                                    list7.append(int(l6))
                                else:
                                    l7 = l6[1:-1]
                                    l7 = l7.split('@')
                                    for l8 in l7:
                                        list8.append(int(l8))
                            list7.append(list8)
                            list6.append(list7)
                        list5.append(list6)
                listAll.append(list5)
        list2 = []


# ## 2-6 bigram query

# In[ ]:


biqu = input('Enter bigram query : ')
for big in AllBigrams:
    a = Bigram([biqu])
    a = a[0]
    for i in big[1]:
        if a == i:
            print(big[0])
            break


# # Step 3

# ## jaccard distance

# In[ ]:


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)


# In[ ]:





# ## Prepare word

# In[ ]:


def prepareWord(WordQuery):
    bad_chars = [';', ':', '!', '*','(',')','[',']','{','}',',','@','-']
    for i in bad_chars :
        WordQuery = WordQuery.replace(i, '') 
    listJaccardDis = []
    for word in AllWords:
        listJaccardDis.append([jaccard_similarity(WordQuery, word),word])
    listJaccardDis.sort()
    return listJaccardDis[-1]


# In[ ]:


prepareWord('رستخیگ')


# ## Prepare query

# In[ ]:


def prepareQuery(Query):
    words = Query.split(' ')
    NewQuery = ""
    listOfDis = []
    for word in words:
        a = prepareWord(word)
        listOfDis.append(a)
        NewQuery += a[1] + " "
    return NewQuery


# ## Calulate tf

# In[ ]:


def calculateTf(w,d):
    counter = 0
    mylist = d.main
    for line in mylist:
        if w in line:
            counter +=(line.count(w))
    return counter


# ## Calulate idf

# In[ ]:


def calculateIdf(w):
    idf = 0
    df = 0
    for word in PositionIndexArray:
        if word.word == w:
            df = len(word.docPositions)
    if(df == 0):
        idf =  math.log(len(docs))
    else:
        idf = math.log(len(docs)/df)
    return idf


# ## calculate tf-idf

# In[ ]:


def calculateTf_Idf(w):
    tf = calculateTf(w)
    idf = calculateIdf(w)
    res = []
    for i in tf:
        i[1] = (i[1]*idf)
        res.append(i)
    return res


# ## tfidf search method 

# In[ ]:


def tfidfSearch(query = '!'):
    if query == '!':
#         query = input('Enter query : ')
        query = 'چو دیده بود حال شود منت سختی دشوار را او رستخیز سخت بود'
        query = prepareQuery(query)
    print('\nnew query : \n'+query+'\n---------')
    terms = query.split(' ')
    terms = terms[:-1]
    terms = list(dict.fromkeys(terms))
    myList = []
    type_of_which_one_that_i_dont_know_what_is_it = input('select type \n1 - lnn-ltn\n2 - lnc-ltc\n\n\t')
    if(type_of_which_one_that_i_dont_know_what_is_it == '2'):
        sumForN = [0]*(len(docs)+1)
    for term in terms:
        i = 0
        cols = []
        tf = query.count(term)
        widf = calculateIdf(term)
        if tf == 0 or tf == 1:
            wtf = 1
        else:
            wtf = 1+math.log(tf)
        w = widf*wtf
        if(type_of_which_one_that_i_dont_know_what_is_it == '1'):
            wn = w
        elif(type_of_which_one_that_i_dont_know_what_is_it == '2'):
            wn = -1
        cols.append(['query',w,wn])
        if(type_of_which_one_that_i_dont_know_what_is_it == '2'):
            sumForN[i] += w**2
        i+=1
        for doc in docs:
            tf = calculateTf(term,doc)
            if tf == 0:
                wtf = 0
            elif tf == 1:
                wtf = 1
            else:
                wtf = 1+math.log(tf)
            w = wtf*1
            if(type_of_which_one_that_i_dont_know_what_is_it == '1'):
                wn = w
            elif(type_of_which_one_that_i_dont_know_what_is_it == '2'):
                wn = -1
            cols.append([doc.id,w,wn])
            if(type_of_which_one_that_i_dont_know_what_is_it == '2'):
                sumForN[i] += w**2
            i+=1
        myList.append(cols)
    if(type_of_which_one_that_i_dont_know_what_is_it == '2'):
        for l in sumForN:
            sumForN[sumForN.index(l)] = math.sqrt(l)
        for l in myList:
            i = 0
            while i < len(l):
                if sumForN[i] == 0 :
                    myList[myList.index(l)][i][2] = 0
                else:
                    myList[myList.index(l)][i][2] = (myList[myList.index(l)][i][1]/sumForN[i])
                i+=1
    scs = [0.0] * len(docs)
    for l in myList:
        q = l[0]
        ds = l[1:]
        for d in ds:
            scs[ds.index(d)] += (q[2] * d[2])
    resss = []
    i = 0
    while i < len(docs):
        resss.append([scs[i],docs[i].id])
        i+=1
    resss.sort(reverse=True)
    return resss


# ## exact search method 

# In[ ]:


def exactSearch():
    res = []
#     query = input('Enter query : ')
    query = 'چو دیده بود حال شود منت سختی دشوار را او رستخیز سخت بود'
    for d in docs:
        for line in d.lines:
            if query in line:
                res.append(d.id)
                break
    return res


# ## get type of search

# In[ ]:


type_of_input = input('Enter number of each one you want :\n1 - tf-idf\n2 - exact search\n\n\t')
if type_of_input == '1':
    result = tfidfSearch()
elif type_of_input == '2':
    result = exactSearch()
else:
    result = []
print(result)


# ## want to see any document???

# In[ ]:


doccc = input('Enter doc id \n\t')
for doc in docs:
    if str(doc.id) == doccc:
        print(doc.lines)
        break


# In[ ]:


with open('PersianPoemsData/RelevanceAssesment/RelevanceAssesment', 'r', encoding="utf-8") as f:
    lines2 = []
    lines = []
    for line in f:
        if line != '\n':
            if('\n' in line):
                line = line[:-1]
                lines.append(line)
            else:
                lines.append(line)
        else:
            lines2.append(lines)
            lines = []
f.close()
for i in range(1,48):
    with open('PersianPoemsData/Queries/'+str(i)+'.persian_query', 'r', encoding="utf-8") as f:
        for line in f:
            res = tfidfSearch(line)
            break
        res2 =res[:50]
        arr8 = lines2[i][1].split(' ')
        relevents = len(arr8)
        retrives = len(res2)
        count1 = 0
        s = 0
        for aar in arr8:
            testA = (aar[:-13])
            for aar2 in res2:
                if testA == str(aar2[1]):
                    count1 +=1
                    s+=(count1/(res2.index(aar2)+1))
        precision = count1/retrives
        recall = count1/relevents
#         b = input('Enter beta: \n\t')
#         b = int(b)
        b = 1
        if recall == 0 and precision == 0 :
            f_m = 0
        else:
            f_m = (((b**2)+1)*precision*recall)/(((b**2)*precision)+recall)
        MAP = s/relevents
        print(f_m)
        print(MAP)
        print(count1)
        print('-----------')
    f.close()


# In[ ]:




