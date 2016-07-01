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
#Return pie chart images for each sample as png format
# REQUIRES R SCRIPT printPieChart.r

import subprocess as sp
import csv

INPUT_FILENAME = 'Genus_Level_Aggregate_Counts.csv'

def main():
	readDataOutput = readData(INPUT_FILENAME)
	listOfSamples = readDataOutput[0]
	listOfGenus = readDataOutput[1]
	aggregateCounts = readDataOutput[2]
	dictOfSamplesTopGenus = makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus)
	isDone = makeEdgeTable(dictOfSamplesTopGenus)


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
	FromNode = []
	ToNode = []
	Weight = []
	
	for listOfSamples in dictOfSamplesTopGenus:
		for listOfMostAbundantGenus in dictOfSamplesTopGenus[listOfSamples]:
			for index in range(length(listOfMostAbundantGenus)):
				#make csv: from Sample to Genus weighted by percent
				FromNode.append(str(listOfSamples))
				ToNode.append(str(listOfMostAbundantGenus[index][0]))
				Weight.append(float(listOfMostAbundantGenus[index][1]) 
	
	with open('MicrobiomeEdges.csv', 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(FromNode)
		filewriter.writerow(ToNode)
		filewriter.writerow(Weight)
	return true

if __name__ == '__main__':
        main()