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

#make pdf
pdf(file = "microbiomenetwork.pdf",width = 8.5, height = 11, onefile= TRUE)

#plotting
net <- graph_from_data_frame(d=links, vertices = nodes, directed=T)
class(net)
colors <- c("lightskyblue", "hotpink1")
V(net)$color <- colors[V(net)$Type]
V(net)$size <- 20
V(net)$label.cex <- 0.75
E(net)$arrow.mode <- 0
plot(net, vertex.color = "cadetblue1",vertex.label.color = "black", vertex.label.family = "Arial Unicode MS", layout = layout_nicely)
dev.off()
