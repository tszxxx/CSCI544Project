#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:01:37 2020

This is for the CSCI 544 Research Project
This script will test the model trained from the movieClassification_perceptron_train.py

@author: Xiwei
"""

import os, sys, string, json

dataSet = "snlp_data"
#inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Test Data/Filtered Data/"+dataSet
inputFolder = "/Users/Xiwei/Desktop/Classes/CS544/Research Project/Model Test Data - Enlarged&Filtered/"+dataSet
classThreshold = 5 # The score which a 'Good' movie should have

######################################
# Read model information
######################################
modelPath = "vanillamodel_"+dataSet+".txt"
modelPath2 = "averagedmodel_"+dataSet+".txt"

'''        
modelInfo = [json.loads(x) for x in open(modelPath, mode = 'r').read().splitlines()]
# Good or Bad
weights = modelInfo[0]
'''
weights = dict()
currentLine = 0
with open(modelPath) as modelInfo:
    for item in modelInfo:
        #print('current Line: '+currentLine)
        if ':' in item:
            key,value = item.split(':', 1)
            value = value.strip('[').replace(']','')
            temp1 =[(x.strip(' ')) for x in value.split(',')]
            weights[key] = float(temp1[0])
        currentLine += 1
        
weights2 = dict()
currentLine = 0
with open(modelPath2) as modelInfo2:
    for item in modelInfo2:
        #print('current Line: '+currentLine)
        if ':' in item:
            key,value = item.split(':', 1)
            value = value.strip('[').replace(']','')
            temp1 =[(x.strip(' ')) for x in value.split(',')]
            weights2[key] = float(temp1[0])
        currentLine += 1


######################################
# Processing testing data
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
Processing Perceptron on dev data
'''
# Different with the training method!!!
def calculateActivation(currentFeature, currentWeights):
    activation  = 0.0

    for token in currentFeature:
        if token in currentWeights:
            activation += currentFeature[token] * currentWeights[token]
        else:
            continue
    return activation + currentWeights['bias']


predictLabel = dict()
predictLabel2 = dict()
outputFile=open("percepoutput_"+dataSet+".txt",'w')
for currentKey, currentVals in devReviews.items():
    if 'DS_Store' not in str(currentKey):
        currentContents = devReviews[currentKey]
        # All in the lower case
        reviewContent = currentContents.translate(None, string.punctuation).lower()
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
            # Here we need to merge the counts in each class
            if token not in inputFeature:
                inputFeature[token] = 1
            else:
                inputFeature[token] += 1
        
        
        # Run perceptron 
        
        # Predicted label by Vanilla
        label_a = ' '
        activation_a = calculateActivation(inputFeature, weights)
        if activation_a > 0:
            label_a = 1
        else:
            label_a = -1
        
        # Predicted label by Averaged
        label_b = ' '
        activation_b = calculateActivation(inputFeature, weights2)
        if activation_b > 0:
            label_b = 1
        else:
            label_b = -1
        
        
        predictLabel[currentKey] = label_a
        predictLabel2[currentKey] = label_b
        # Write to the output file
        outputFile.write(str(label_a)+" "+str(currentKey))
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

tp_b = 0
tn_b = 0
fp_b = 0
fn_b = 0

for currentKey, currentVals in devLabels.items():
    if 'DS_Store' not in str(currentKey):
        # Predict labels
        pLabel_a = predictLabel[currentKey]
        pLabel_b = predictLabel2[currentKey]
        
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
            
        if dLabel_a == 1 and pLabel_b == dLabel_a:
            tp_b += 1
        elif dLabel_a == 1 and pLabel_b != dLabel_a:
            fn_b += 1
        elif dLabel_a == -1 and pLabel_b == dLabel_a:
            tn_b += 1
        elif dLabel_a == -1 and pLabel_b != dLabel_a:
            fp_b += 1

        count += 1

print("Vanilla Results below: ")
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

print(" ")
print("Averaged Results below: ")
print('True Positive: ' + str(tp_b)) 
print('True Negative: ' + str(tn_b)) 
print('False Positive: ' + str(fp_b)) 
print('False Negative: ' + str(fn_b)) 

if tp_b + fp_b != 0:
    precision_b = float(tp_b) / (tp_b + fp_b)
else:
    precision_b = 0

if tp_b + fn_b != 0:
    recall_b = float(tp_b) / (tp_b + fn_b)
else:
    recall_b = 0

print('Precision: ' + str(precision_b))
print('Recall: ' + str(recall_b))

if precision_b + recall_b != 0:
    f1_b = 2 * precision_b * recall_b / (precision_b + recall_b)
else:
    f1_b = 0

print('Mean F1: ' + str(f1_b))
