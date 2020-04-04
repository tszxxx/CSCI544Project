#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 20:38:37 2020

This is for the CSCI 544 Research Project
This script will learn a naive Bayes model from the training data

@author: Xiwei
"""

import os, sys, string, copy
# inputFolder = sys.argv[-1]
dataSet = "char_data"
# inputFolder = '/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Input Data/Filtered Data/' + dataSet
inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Input Data - Enlarged&Filtered/"+dataSet
#inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Input Data/"+dataSet
classThreshold = 5 # The score which a 'Good' movie should have

######################################
# Preprocessing input data
######################################
stopWords = {}
# Create a dictionary and use the file name as the identical key
labels = {}
reviews = dict()

'''
Preprocessing functions
'''
def assignLabels(currentKey, currentLabel, currentContents):
    
    # Good or Bad
    if (labels.get(currentKey)) == 1:
        countTokens(currentContents, 0)
    if (labels.get(currentKey)) == -1:
        countTokens(currentContents, 1)
            
reviewToken = dict()   
# 2 indices: Good / Bad    
def countTokens(contents, labelIndex):
    for token in contents:
        # Remove stop words - added by Xiwei
        if token not in stopWords:
            if (reviewToken.has_key(token)): # Already exist
                reviewToken[token][labelIndex] += 1
            else: # Claim new
                reviewToken[token] = [0,0]
                reviewToken[token][labelIndex] += 1
            
'''
Start read the files
'''
for dirpath, dirnames, files in os.walk(inputFolder):
    if 'DS_Store' not in str(dirpath):
        for currentFile in files:
            if 'DS_Store' not in str(currentFile):
                fileName = str(currentFile)
                tempScore = fileName[0]
                if int(tempScore) > classThreshold:
                    currentLabel = 1 # Good one
                elif int(tempScore) <= classThreshold:
                    currentLabel = -1 # Bad one
                else:
                    print("Something wrong in the assign label part")
                
                f = open(dirpath + '/' + currentFile, 'r')
                currentContents = f.read()
                reviews[fileName] = currentContents
                labels[fileName] = currentLabel
            
'''
Processing labels and words (tokens)
'''
for fileName in reviews:
    reviewContent = reviews[fileName]
    reviewLabel = labels[fileName]
    
    # All in the lower case
    reviewContent = reviewContent.translate(None, string.punctuation).lower()
    # Split into tokens
    # temp = [word for word in reviewContent.split() if (word.isalnum())] # No suit for chinese!!!
    
    # tempWord = [word for word in reviewContent.split() if (word.isalnum())] # Count repeated words
    tempWord = []
    for word in reviewContent.split():
        if word not in tempWord: # Don't count repeated words
            tempWord.append(word)
    
    tokenList = ' '.join(tempWord)
    tokenList = ''.join([i for i in tokenList if not i.isdigit()])
    tokenList = tokenList.split()
    
    # Assign Labels to those tokens
    assignLabels(fileName, reviewLabel, tokenList)

'''
Smoothing
'''        
for currentKey,currentVals in reviewToken.items():
    for i in range(0,2):
        reviewToken[currentKey][i] += 1
       
######################################
# Train the Naive Bayes model
######################################
'''
Prior Probability
'''
totalGood, totalBad = 0, 0
for currentKey, currentVals in reviewToken.items():
    totalGood += currentVals[0]
    totalBad += currentVals[1]

    
priorGood = float(totalGood) / (totalGood + totalBad)
priorBad = float(totalBad) / (totalGood + totalBad)

    
'''
Training Data Probability
'''
reviewProb = copy.deepcopy(reviewToken)
for currentKey, currentVals in reviewToken.items():
    reviewProb[currentKey][0] = float(reviewToken[currentKey][0]) / totalGood
    reviewProb[currentKey][1] = float(reviewToken[currentKey][1]) / totalBad

 
######################################
# Save the Naive Bayes Model into file
######################################    
# write to a model
with open("nbmodel_"+dataSet+".txt", 'w') as f:
   f.write("Prior Class Probabilities:"+'\n')
   f.write('good:'+str(priorGood)+'\n')
   f.write('bad:'+str(priorBad)+'\n')
   f.write("Tokens Probabilities:"+'\n')
   for currentKey, currentVals in reviewProb.items():
        f.write('%s:%s\n' % (currentKey, currentVals))
        
with open("reviewToken_"+dataSet+".txt", 'w') as f:
    f.write("Review Token Distribution:"+'\n')
    for currentKey, currentVals in reviewToken.items():
        f.write('%s:%s\n' % (currentKey, currentVals))