

#!/usr/bin/Rscript
#
#produce the microbiome network
#by: Hannah Voelker, Jul 5, 2016

rm(list = ls())
library(igraph)
library(extrafont)

#import the csv files we produced in python
nodes <<- read.csv(file.choose(), header = TRUE, as.is = T)
links <<- read.csv(file.choose(), header = TRUE, as.is = T)

#next, manipulate the data to make it ready for the graph
head(nodes)
head(links)
nrow(nodes); length(unique(nodes$id))
nrow(links); nrow(unique(links[,c("From", "To")]))

#get rid of duplicates in the "nodes" data frame
nodes <- unique(nodes)

#plotting
net <- graph_from_data_frame(d=links, vertices = nodes, directed=T)
class(net)
plot(net)
