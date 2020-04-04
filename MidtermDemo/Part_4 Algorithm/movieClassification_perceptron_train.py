#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:49:08 2020

This is for the CSCI 544 Research Project
This script will learn a perceptron model from the training data

@author: Xiwei
"""

import os, sys, string, json

dataSet = "snlp_data"
#inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Input Data/Filtered Data/"+dataSet
inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Input Data - Enlarged&Filtered/"+dataSet

classThreshold = 5 # The score which a 'Good' movie should have
######################################
# Preprocessing input data
######################################
'''
Stop words
'''
# Define a set of stop words for improving the modeling performance
# Ref: https://nlp.stanford.edu/IR-book/html/htmledition/dropping-common-terms-stop-words-1.html
'''
stopWords = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'below', 'his', 'or', 'such',
             'for', 'from', 'has', 'he', 'her', 'in', 'is', 'it', 'its', 'my', 'our', 'they',
             'of', 'on', 'she', 'that', 'the', 'to', 'was', 'were', 'will', 'with', 'which'}
'''
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

        
######################################
# Train the Perceptron model
######################################  
'''
Claim functions
'''
def weightsUpdating_vanilla(currentFeature, currentWeights, label):
    for token in currentFeature:
        currentWeights['Vanilla'][token] += label * currentFeature[token]
        
    currentWeights['Vanilla']['bias'] += label;     
        
def weightsUpdating_averaged(currentFeature, currentWeights, label, tokenCount):
    for token in currentFeature:
        currentWeights['Averaged'][token] += label * currentFeature[token] * tokenCount
        
    currentWeights['Averaged']['bias'] += label * tokenCount      
    
def calculateActivation(currentFeature, currentWeights):
    activation  = 0.0

    for token in currentFeature:
        if token in currentWeights['Vanilla']:
            activation += currentFeature[token] * currentWeights['Vanilla'][token]
        else:
            currentWeights['Vanilla'][token] = 0
            currentWeights['Averaged'][token] = 0
            activation += 0
    return activation + currentWeights['Vanilla']['bias']

def calculateAveragedPerceptron(weights, weightsAvg, tokenCount):
    for token in weightsAvg:
        weightsAvg[token] = weights[token] - (float(weightsAvg[token])/tokenCount)
'''
Claim variables
'''
# Weights for good or bad
weights = {'Vanilla':{'bias':0.0}, 'Averaged':{'bias':0.0}}
# For averaging weights
tokenCount = 1
# Maximum iteration number
maxIter = 30
# Current step count
step = 0

'''
Start iterations
'''
while(step < maxIter):
    
    for fileName in reviews:
        reviewContent = reviews[fileName]
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
        
        # Get feature
        inputFeature = dict()

        for token in tokenList:
            if token not in stopWords:
                # Count the token appearance
                if inputFeature.has_key(token):
                    inputFeature[token] += 1
                else:
                    inputFeature[token] = 1
            
        currentLabel = labels[fileName] # Good or Bad
            
        # Calculate activation for both labels: TD and PN
        currentActivation = calculateActivation(inputFeature, weights)

        
        # good or bad
        if currentLabel * currentActivation <= 0:
            weightsUpdating_vanilla(inputFeature, weights, currentLabel)
            weightsUpdating_averaged(inputFeature, weights, currentLabel, tokenCount)
            
            
        tokenCount += 1
    
    step += 1
    
# For the averaged perception
calculateAveragedPerceptron(weights['Vanilla'], weights['Averaged'], tokenCount)
    
''' 
Output to File
'''
# write to a model
with open("vanillamodel_"+dataSet+".txt", 'w') as f:
   for currentKey, currentVals in weights['Vanilla'].items():
        f.write('%s:%s\n' % (currentKey, currentVals))
        
with open("averagedmodel_"+dataSet+".txt", 'w') as f:
   for currentKey, currentVals in weights['Averaged'].items():
        f.write('%s:%s\n' % (currentKey, currentVals))
'''        
writeFilePath = "vanillamodel_"+dataSet+".txt"
writeFile = open(writeFilePath, mode = 'w')
writeFile.write(json.dumps(weights['Vanilla']))
writeFile.write("\n")
    
writeFilePath = "averagedmodel_"+dataSet+".txt"
writeFile = open(writeFilePath, mode = 'w')
writeFile.write(json.dumps(weights['Averaged']))
writeFile.write("\n")
'''