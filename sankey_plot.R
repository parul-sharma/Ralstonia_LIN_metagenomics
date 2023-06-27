if(!require(networkD3)) install.packages("networkD3", repos = "http://cran.us.r-project.org")
library(networkD3)
args <- commandArgs(trailingOnly=TRUE)

if (length(args) != 1) {
  cat("Usage: Rscript sankey_plot.R input_file\n Add complete path to input file!")
  quit(save = "no", status = 1)
}

input_file <- args[1]
input <- read.delim(input_file, sep =',')

##input <- read.delim("~/Desktop/LIN-kraken/Ralstonia/Sankey-plots/brc1_c0.finalLINoutput.txt")

###Getting the list of names in the data:


a=input$LINgroup_Name  ##stores all the LINgroups in a list
a=as.character(a)
name=unlist(strsplit(a, ';'))  #stores all the broken down list of LINgroup categories by splitting on ';'

##only retain the unique LINgroups categories
name = unique(name)
nodes = data.frame(name)

###creating a dictionary of 'name' to help create source and target lists 
vals <- 0:length(name)
keys <- name
##linking vals to keys in R is done using names function..python equivalent of dict
names(vals) <-keys

#####finding source and target and value lists
source = c()
target = c()
value = c()
for (i in 1:nrow(input))
{ 
  x=as.list(unlist(strsplit(as.character(input[i,'LINgroup_Name']),';')))
  x
  if(length(x) > 1)
  { source = append(source, vals[[x[[length(x)-1]]]])  ##adding corresponding int value using vals dictionary 
    target = append(target, vals[[x[[length(x)]]]])  ##adding corresponding int value using vals dictionary 
    value = append(value, input[i,'Assigned_reads'])
  } 
  #else    ###this will be the case of total reads with only 1 category of LINgroups
 # { source = vals[x[-1]]  ##adding corresponding int value using vals dictionary 
  #  target = vals[x[-1]]  ##adding corresponding int value using vals dictionary 
  #  value = input[i,'Assigned_reads']
  #}
}  


links = data.frame(source,target,value)
##Remove rows from df where abundance is zero!!
links = links[links$value != 0, ]
##order the df by source so the linkage is proper
links = links[order(links$source),]  ##this introduced NA in the dataframe
###links = links[links$source != NA, ]  ##cleaning NAs


df=list(nodes,links)
q <- sankeyNetwork(Links = links, Nodes = nodes, Source = "source",
                   Target = "target", Value = "value", NodeID = "name",
                   units = "", fontSize = 12, nodeWidth = 30, sinksRight = FALSE)


saveNetwork(q, "plot.html")
