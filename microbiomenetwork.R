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
pdf(file = "microbiomenetwork.pdf",width = 20, height = 20, onefile= TRUE)

#plotting
net <- graph_from_data_frame(d=links, vertices = nodes, directed=T)
class(net)
colrs <- c("lightskyblue", "hotpink1")
V(net)$color <- colrs[V(net)$node.type]
V(net)$size <- 14
V(net)$label.cex <- 0.8
E(net)$width <- E(net)$Weight/6
E(net)$arrow.mode <- 0

plot(net,vertex.label.color = "black", vertex.label.family = "Arial Unicode MS", layout = layout_nicely)
legend(x=1.5, y=1.1, c("Sample", "Genus"), pch=21,
       col="#777777", pt.bg=colrs, pt.cex=2, cex=.8, bty="n", ncol=1)
dev.off()
