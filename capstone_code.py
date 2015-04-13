import matplotlib.pyplot as plt
import numpy as np
import urllib
import nltk
import re
import os

pathToSets = '..' + os.sep + 'Capstone Project' + os.sep + 'sets'
pathToScores = '..' + os.sep + 'Capstone Project' + os.sep + 'scores'
dirWordLists = '..' + os.sep + 'Capstone Project' + os.sep +'word_lists' 

#get the concept vectors (or the words that we are searching for) from the txt file
def getConceptVectors():
    f = open('conceptvectors.txt','r').read()
    f = f.split('\n')
    return(f)

#this calculates the frequency of words (absolute)
def calculateWordFreq(setName,option):
    conceptVectors = getConceptVectors()
    setLocation = pathToSets + os.sep + setName
    file_list = os.listdir(setLocation)
    just_counts_Dict= {}
    file_list.remove('.DS_Store')
    file_list.sort()
    countHits = []
    for i in list(range(len(file_list))):
        file_read = open(os.path.join(setLocation, file_list[i]), 'r').read()
        file_read = nltk.clean_html(file_read)
        vector_count = []
        just_counts = []
        file_read_count = []
        for j in list(range(len(conceptVectors))):
            txtCount = 0
            txtCount = len(re.findall(conceptVectors[j],file_read,flags = re.IGNORECASE))
            file_read_count.append(len(re.findall(conceptVectors[j],file_read,flags = re.IGNORECASE)))
            vector_count.append((conceptVectors[j],txtCount))
        just_counts.append(file_read_count)
        countHits.append((file_list[i],vector_count))
        just_counts_Dict[file_list[i]] = just_counts
    if option == 0:
        return(countHits)
    elif option == 1:
        return(just_counts_Dict)

#this calculates the frequency of words (Normalized)
def calculateNormWordFreq(setName,option):
    conceptVectors = getConceptVectors()
    setLocation = pathToSets + os.sep + setName
    file_list = os.listdir(setLocation)
    file_list.remove('.DS_Store')
    file_list.sort()
    countHits = []
    just_counts_Dict = {}
    for i in list(range(len(file_list))):
        file_read = open(os.path.join(setLocation, file_list[i]), 'r').read()
        file_read = nltk.clean_html(file_read)
        vector_count = []
        just_counts = []
        file_read_count = []
        file_total_words = float(len(file_read.split()))
        for j in list(range(len(conceptVectors))):
            txtCount = 0
            txtCount = (len(re.findall(conceptVectors[j],file_read,flags = re.IGNORECASE))/(file_total_words))*100000.0
            file_read_count.append((len(re.findall(conceptVectors[j],file_read,flags = re.IGNORECASE))/(file_total_words)) * 100000.0)
            vector_count.append((conceptVectors[j],txtCount))
        just_counts.append(file_read_count)
        countHits.append((file_list[i],vector_count))
        just_counts_Dict[file_list[i]] = just_counts
    if option == 0:
        return(countHits)
    elif option == 1:
        return(just_counts_Dict)
        
def writeCSVWordFreqScores(function):
    daData = function
    import string
    alphabet = list(string.ascii_lowercase)
    if function == calculateWordFreq('trainingset',0):
        f = open('wordFreqScores.txt', 'w')
        f.write('Company')
        for i in list(range(len(daData[0][1]))):
            f.write(',' + str(daData[0][1][i][0]))
        f.write(',' + 'SUM' + '\n')
        for j in list(range(len(daData))):
            f.write(str(daData[j][0][:-9]) + ',')
            for n in list(range(len(daData[0][1]))):
                f.write(str(daData[j][1][n][1]) + ',')
            f.write('=SUM(B' + str(j+2) + ':K' + str(j+2) + ')' + '\n')
        f.write('SUM' + ',')
        for k in alphabet[1:16]:
            f.write('=SUM(' + str(k) + '2:' + str(k) + '31)' + ',') 
        f.close()
        print('Done writing file wordFreqScores.txt')
    elif function == calculateNormWordFreq('trainingset',0):
        f = open('wordNormFreqScores.txt', 'w')
        f.write('Company')
        for i in list(range(len(daData[0][1]))):
            f.write(',' + str(daData[0][1][i][0]))
        f.write(',' + 'SUM' + '\n')
        for j in list(range(len(daData))):
            f.write(str(daData[j][0][:-9]) + ',')
            for n in list(range(len(daData[0][1]))):
                f.write(str(daData[j][1][n][1]) + ',')
            f.write('=SUM(B' + str(j+2) + ':K' + str(j+2) + ')' + '\n')
        f.write('SUM' + ',')
        for k in alphabet[1:16]:
            f.write('=SUM(' + str(k) + '2:' + str(k) + '31)' + ',') 
        f.close()
        print('Done writing file wordNormFreqScores.txt')

def sentExtract(setName):
    conceptVectors = getConceptVectors()
    setLocation = pathToSets + os.sep + setName
    file_list = os.listdir(setLocation)
    file_list.remove('.DS_Store')
    file_list.sort()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    #sentenceEnds = re.compile('[.!?][\s]{1,2}(?=[A-Z])')
    file_list_vector_count = []
    just_counts = []
    final_dict = {}
    for i in list(range(len(file_list))):
        file_read = open(os.path.join(setLocation, file_list[i]), 'r').read()
        file_read =re.sub(r'\n',' ',file_read)
        #sentenceList = sentenceEnds.split(file_read)
        file_read = nltk.clean_html(file_read)
        sentenceList = tokenizer.tokenize(file_read)
        vector_count = []
        file_read_count = []
        sent_dict = {}
        for j in list(range(len(conceptVectors))):
            foundword_sentence_list = [] #list of sentences with the word in the sentence
            sentence_count = 0
            for n in list(range(len(sentenceList))):
                if re.findall(conceptVectors[j],sentenceList[n],flags = re.IGNORECASE) != []:
                    foundword_sentence_list.append(sentenceList[n])
            sent_dict[conceptVectors[j]] = foundword_sentence_list
        final_dict[file_list[i]] = sent_dict
    return(final_dict)
                #sentence_count = len(foundword_sentence_list)
            #file_read_count.append(sentence_count)
            #vector_count.append((conceptVectors[j],sentence_count))
        #just_counts.append((file_read_count))
        #file_list_vector_count.append((file_list[i],vector_count))
    #return(file_list_vector_count)
    #return(just_counts)


def getScores():
    scoresLocation = pathToScores + os.sep + 'newsweek_scores_2010.csv'
    f = open(scoresLocation,'r').read()
    f = f.replace('"','')
    f = f.split('\r')
    f = [f[i].split('|') for i in list(range(len(f)))]
    #for j in list(range(len(f))):
    #    f[j][0] = f[j][0].replace('-',' ')
    #    f[j][0] = f[j][0].replace('!','')
    return(f)
    
def matchScores():
    scores = getScores()
    matchedScores_Dict = {}
    trainingSetLocation = pathToSets + os.sep + 'trainingset'
    file_list = os.listdir(trainingSetLocation)
    file_list.remove('.DS_Store')
    file_list.sort()
    file_list_names = [file_list[i][:-9] for i in list(range(len(file_list)))]
    #file_list_names = [file_list_names[j].replace('-',' ') for j in list(range(len(file_list_names)))]
    #file_list_names = [file_list_names[n].replace('!', '') for n in list(range(len(file_list_names)))]
    file_list_names = filter(None, file_list_names)
    for j in list(range(len(file_list_names))):
        for i in list(range(len(scores))):
            if re.findall(file_list_names[j], scores[i][0]) != []:
                matchedScores_Dict[file_list[j]] = scores[i][1:]
    return(matchedScores_Dict)
    
def writeCSVRegression():
    wordFreq = calculateWordFreq('trainingset',1)
    normWordFreq = calculateNormWordFreq('trainingset',1)
    scores = matchScores()
    f = open('Regression.txt', 'w')
    f.write('Company,' + '# Sustainability Words,' + 'Newsweek Score\n')
    companies = sorted(wordFreq.keys())
    for i in companies:
        f.write(str(i[:-9]) + ',' + str(sum(wordFreq[i][0])) + ',' + str(scores[i][1]) + '\n')
    f.write('\n\n')
    f.write('Company,' + '# Sustainability Words,' + 'Newsweek Score\n')
    for j in companies:
        f.write(str(j[:-9]) + ',' + str(sum(normWordFreq[j][0])) + ',' + str(scores[j][1]) + '\n')
    f.close()
    print('Done writing file Regression.txt')
    
    
def sentenceSentiment(option): #option = 0 or 1 
    from nltk.tokenize.punkt import PunktWordTokenizer
    urlneg = 'http://www.unc.edu/~ncaren/haphazard/negative.txt'
    urlpos = 'http://www.unc.edu/~ncaren/haphazard/positive.txt'
    urllib.urlretrieve(urlneg,dirWordLists + os.sep + 'negative.txt')
    urllib.urlretrieve(urlpos,dirWordLists + os.sep + 'positive.txt')
    neg_list = open(dirWordLists + os.sep + 'negative.txt').read()
    pos_list = open(dirWordLists + os.sep + 'positive.txt').read()
    neg_list = sorted(list(set(neg_list.split('\n'))))
    neg_list = filter(None, neg_list)
    pos_list = sorted(list(set(pos_list.split('\n'))))
    pos_list = filter(None, pos_list)
    sent_Dict_sentiment = sentExtract('trainingset')
    sent_Dict = sentExtract('trainingset')
    setLocation = pathToSets + os.sep + 'trainingset'
    file_list = os.listdir(setLocation)
    file_list.remove('.DS_Store')
    file_list.sort()
    conceptVectors = getConceptVectors()
    for i in file_list:
        for j in conceptVectors:
            for n in list(range(len(sent_Dict[i][j]))):
                pos_count = 0
                neg_count = 0
                words = PunktWordTokenizer().tokenize(sent_Dict[i][j][n])
                for word in words:
                    if word in pos_list:
                        pos_count+=1
                    elif word in neg_list:
                        neg_count+=1
                sent_Dict_sentiment[i][j][n] = (pos_count, neg_count)
    if option == 0: #calculate overall positive and negative scores for documents
        return(sent_Dict_sentiment)
    elif option == 1: #calculate positive and negative separately for each document
        sent_Dict_Sum_sentiment = {}
        for x in file_list:
            total_pos = 0
            total_neg = 0
            for y in conceptVectors:
                for z in list(range(len(sent_Dict_sentiment[x][y]))):
                    total_pos += sent_Dict_sentiment[x][y][z][0]
                    total_neg += sent_Dict_sentiment[x][y][z][1]
            sent_Dict_Sum_sentiment[x] = [total_pos,total_neg]
        return(sent_Dict_Sum_sentiment)

def findIndustry():
    scores = getScores()
    industry_Dict = {}
    trainingSetLocation = pathToSets + os.sep + 'trainingset'
    file_list = os.listdir(trainingSetLocation)
    file_list.remove('.DS_Store')
    file_list.sort()
    file_list_names = [file_list[i][:-9] for i in list(range(len(file_list)))]
    file_list_names = filter(None, file_list_names)
    for j in list(range(len(file_list_names))):
        for i in list(range(len(scores))):
            if re.findall(file_list_names[j], scores[i][0]) != []:
                industry_Dict[file_list_names[j]] = scores[i][1]
    return(industry_Dict)

def writeCSVSentenceSentiment():
    f = open('sentenceSentimentScores.txt', 'w')
    daData = sentenceSentiment(1)
    keys = sorted(daData.keys())
    industry_Dict = findIndustry()
    import string
    alphabet = list(string.ascii_lowercase)
    f.write('Company' + '|' + 'Industry' + '|' + 'Positive' + '|' + 'Negative' +'\n')
    for i in keys:
        f.write(str(i[:-9]) + '|' + industry_Dict[i[:-9]] + '|' + str(daData[i][0]) + '|' + str(daData[i][1]) + '\n')
    f.write('SUM' + '|' + ' |')
    for k in alphabet[2:4]:
        f.write('=SUM(' + str(k) + '2:' + str(k) + '31)' + '|') 
    f.close()
    print('Done writing file sentenceSentimentScores.txt')
