#!/usr/bin/Rscript
#
#produce the microbiome network
#by: Hannah Voelker, Jul 5, 2016

rm(list = ls())
library(igraph)
library(extrafont)

#import the csv files we produced in python
nodes <<- csvread(file.choose(), header = TRUE, sep = ",")
edges <<- csvread(file.choose(), header = TRUE, sep = ",")

#next, manipulate the data to make it ready for the graph

#plotting

