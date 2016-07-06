#Microbiome-graph

Produces a network of given microbiome data

_These programs were written for the [BioSeq](http://ase.tufts.edu/chemistry/walt/sepa/index.html) program at Tufts University, as part of Hannah's summer research project on the microbiomes of various probiotics._

###Step 1: Node and edge table production in Python

This python script uses an input CSV of aggregate counts for each genus of bacteria found in a set of samples. 

Utilizing this CSV file, a dictionary is made: The key being a sample name, and for each key, a set of ten tuples are made, with the first value being the Genus, and the second value being a float of the percent abundance in the sample.

The edges table has the following: From Node, To Node, and Weight.
The node table has the following: Node, Type (Sample vs OTU)

Iterating through this dictionary, two CSV files are written and exported: one for the edge table, and one for the node table.

###Step 2: Producing an aesthetically pleasing graph in R 

Using the csv files produced in Python, and the iGraph package in R, a weighted graph is produced.
_Requirements: installation of the igraph and extrafont packages_
