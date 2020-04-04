#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 20:38:37 2020

This is for the CSCI 544 Research Project
This script will test the trained naive Bayes model with the testing data

@author: Xiwei
"""

import os, sys, string, math, random

# inputFolder = sys.argv[-1]
dataSet = 'char_data'
# inputFolder = '/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Test Data/Filtered Data/' + dataSet
inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Test Data - Enlarged&Filtered/"+dataSet
#inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Test Data/"+dataSet

'''
Caution, this threshold should be the main as in the training script!!
'''
classThreshold = 5 # The score which a 'Good' movie should have

######################################
# Read model information
######################################
#reading from nbmodel.txt
reviewProb = dict()
priorInfo = dict()
currentLine = 0
with open("nbmodel_"+dataSet+".txt") as modelInfo:
    for item in modelInfo:
        #print('current Line: '+currentLine)
        if ':' in item:
            key,value = item.split(':', 1)
            # For prior information
            if(currentLine<=2):
                priorInfo[key] = value.strip(' ')
            # For token probabilities
            else:
                value = value.strip('[').replace(']','')
                reviewProb[key] =[(x.strip(' ')) for x in value.split(',')]
        currentLine += 1

# Prior probabilities
priorGood = float(priorInfo['good'])
priorBad = float(priorInfo['bad'])

######################################
# Processing Testing data
######################################

'''
Start read the files
'''
devReviews = dict()
devLabels = dict()
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
                devReviews[fileName] = currentContents
                devLabels[fileName] = currentLabel
            
'''
Processing Naive Bayes on dev data
'''
predictLabel = dict()
# Delte the previous output file
try:
    os.remove("nboutput.txt")
except:
    print('')
    
outputFile=open("nboutput.txt",'w')
for currentKey, currentVals in devReviews.items():
    if 'DS_Store' not in str(currentKey):
        currentContents = devReviews[currentKey]
        # All in the lower case
        reviewContent = currentContents.translate(None, string.punctuation).lower()
        # Split into tokens
        # tempWord = [word for word in reviewContent.split() if (word.isalnum())] # Count repeated words
        tempWord = []
        for word in reviewContent.split():
            if word not in tempWord: # Don't count repeated words
                tempWord.append(word)
                
        tokenList = ' '.join(tempWord)
        tokenList = ''.join([i for i in tokenList if not i.isdigit()])
        tokenList = tokenList.split()
         
        ######################################
        # Calculate test token prob
        ######################################
        # Initial
        probGood = 0.0
        probBad = 0.0
        
        for token in tokenList:
            # For seen token
            if (reviewProb.has_key(token)):
                # Change to log scale '+' instead of '*' - Note: Need smoothing here!!!
                temp = reviewProb[token][0]
                #print(temp)
                probGood += math.log(float(temp))
                temp = reviewProb[token][1]
                probBad += math.log(float(temp))
        
        # Plus the prior probabilities
        probGood_final = probGood + math.log(priorGood)
        probBad_final = probBad + math.log(priorBad)
            
        label_a = 0 # Good or Bad
                
        if probGood_final > probBad_final:
            label_a = 1
            printLabel = 'Good'
        else:
            label_a = -1
            printLabel = 'Bad'
        
        predictLabel[currentKey] = label_a
        # Write to the output file
        outputFile.write(printLabel+" "+str(currentKey))
        outputFile.write('\n')
        
        
######################################
# Measure performance
        # Note: We can use this for dev set but we can't use this on Vocareum
        # Since all the folder name and file names are masked
###################################### 

print("Measuring Performance below: ")
print('For local development set testing only')
count = 0

tp_a = 0 # True Positive
tn_a = 0 # True Negative
fp_a = 0 # False Positive
fn_a = 0 # False Negative

for currentKey, currentVals in devLabels.items():
    if 'DS_Store' not in str(currentKey):
        # Predict labels
        pLabel_a = predictLabel[currentKey]
        
        # Desired labels
        dLabel_a = devLabels[currentKey]
        
        # For label a: Good or Bad
        if dLabel_a == 1 and pLabel_a == dLabel_a:
            tp_a += 1
        elif dLabel_a == 1 and pLabel_a != dLabel_a:
            fn_a += 1
        elif dLabel_a == -1 and pLabel_a == dLabel_a:
            tn_a += 1
        elif dLabel_a == -1 and pLabel_a != dLabel_a:
            fp_a += 1

        count += 1

print('True Positive: ' + str(tp_a)) 
print('True Negative: ' + str(tn_a)) 
print('False Positive: ' + str(fp_a)) 
print('False Negative: ' + str(fn_a)) 

if tp_a + fp_a != 0:
    precision_a = float(tp_a) / (tp_a + fp_a)
else:
    precision_a = 0

if tp_a + fn_a != 0:
    recall_a = float(tp_a) / (tp_a + fn_a)
else:
    recall_a = 0

print('Precision: ' + str(precision_a))
print('Recall: ' + str(recall_a))

if precision_a + recall_a != 0:
    f1_a = 2 * precision_a * recall_a / (precision_a + recall_a)
else:
    f1_a = 0

print('Mean F1: ' + str(f1_a))