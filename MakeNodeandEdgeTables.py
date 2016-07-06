#!usr/bin/env python

#MakeNodeandEdgeTables.py
#Author: Hannah Voelker
#Made: 6/29/16

#Given a spreadsheet of counts for various genus (or other OTU level) for each sample
# Format as shown:
#Genus,MH01-A,MH95HP,MH10-B, ...
#Streptococcus,38,79115,6225, ...
#Propionibacterium,26,3,36045, ...
#Staphylococcus,5,3,6028, ...
#...
# (Note: This type of file is available from the BaseSpace 16S Metagenomics App.)
#
#Return edge and node tables for use 

import subprocess as sp
import csv

INPUT_FILENAME = 'Genus_Level_Aggregate_Counts.csv'

def main():
	readDataOutput = readData(INPUT_FILENAME)
	listOfSamples = readDataOutput[0]
	listOfGenus = readDataOutput[1]
	aggregateCounts = readDataOutput[2]
	dictOfSamplesTopGenus = makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus)
	makeEdgeTable(dictOfSamplesTopGenus)
	makeNodeTable(dictOfSamplesTopGenus)


def readData(INPUT_FILENAME):
	#read in sample names, genus names, and aggregate counts
	with open(INPUT_FILENAME, 'r') as filer:
		listOfSamples = filer.readline().strip().split(',')[1:]
		listOfGenus = []
		aggregateCounts = []
		for line in filer:
			currentLine = line.strip().split(',')
			listOfGenus.append(currentLine[0])
			aggregateCounts.append(currentLine[1:])
	aggregateCounts = map(list, zip(*aggregateCounts)) #transpose the aggregate counts
	aggregateCounts = [map(int, x) for x in aggregateCounts] #convert aggregate counts to int
	return (listOfSamples, listOfGenus, aggregateCounts)

def makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus):
#convert aggregate counts to presence/absence calls for each genus
#make a list of sets, each set contains the ten most abundent genus in each sample
#requires aggregateCounts, listOfGenus, listOfSamples
	listOfMostAbundantGenus = []
	for samplewiseAggregateCounts in aggregateCounts:
		listOfMaxValueIndexes = []
		mostAbundantGenus = []#initializes the list that will contain the 10 most abundent genus
		totalAggregateCounts = sum(samplewiseAggregateCounts)		
		for x in range(10):
			highestNumOfAggregateCounts = max(samplewiseAggregateCounts)
			currIndex = samplewiseAggregateCounts.index(highestNumOfAggregateCounts)
			mostAbundantGenus.append((listOfGenus[currIndex],float(highestNumOfAggregateCounts)/float(totalAggregateCounts)))
			samplewiseAggregateCounts[currIndex] = 0 #percentages after this 
		listOfMostAbundantGenus.append(mostAbundantGenus)
		listOfMostAbundantGenus.sort(reverse= True) #ensures we sorted correctly
	#zip these sets into a dictionary {key = sample name: value = set of most abundant genus}
	dictOfSamplesTopGenus = dict(zip(listOfSamples,listOfMostAbundantGenus))
	return dictOfSamplesTopGenus

def makeEdgeTable(dictOfSamplesTopGenus):
	#makes the edge table: from Sample to Genus Weighted by percentage
	outputFile = open('MicrobiomeEdges.csv', 'w')
	filewriter = csv.writer(outputFile)
	rowvector = []
	header = ['From', 'To', 'Weight']
	filewriter.writerow(header)
	for key in dictOfSamplesTopGenus:
		for listOfMostAbundantGenus in dictOfSamplesTopGenus[key]:
				#make the vectors from Sample to Genus weighted by percent
				rowvector = [str(key), str((listOfMostAbundantGenus[0])), float(100*listOfMostAbundantGenus[1])]
				filewriter.writerow(rowvector)


def makeNodeTable(dictOfSamplesTopGenus):
	outputFile = open('MicrobiomeNodes.csv', 'w')
	filewriter = csv.writer(outputFile)
	rowvector = []
	header = ['Node', 'node.type', 'node.label']
	filewriter.writerow(header)

	#first loop through keys and get sample names
	for key in dictOfSamplesTopGenus:
		rowvector = [str(key), 1, 'Sample']
		filewriter.writerow(rowvector)

	#now take the OTU's
	for key in dictOfSamplesTopGenus:
		for listOfMostAbundantGenus in dictOfSamplesTopGenus[key]:
				rowvector = [str(listOfMostAbundantGenus[0]), 2, 'Genus']
				filewriter.writerow(rowvector)
	

if __name__ == '__main__':
        main()
