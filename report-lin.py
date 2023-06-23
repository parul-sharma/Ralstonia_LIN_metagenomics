#!/bin/python

'''USAGE: ./report-lin.py lingroups.txt taxonomy/data.txt input.report'''

import sys
import pandas as pd
import argparse

#Function to convert string to List
def convert_LIN_string(LIN):
	LIN_string=LIN.split(",")
	return LIN_string


def find_taxid_of_lingroup(lingroup, data):
	similarLIN = [i for i in data['LIN'] if lingroup in i] #using list comprehension to get string with substring 
	top_LIN=similarLIN[0] #select the first best match
	index = data[data['LIN']==top_LIN].index.values #indeex of top LIN
	index = int(index)
	taxids = data['taxid_LIN'][index] # taxids of the top LIN
	taxids = convert_LIN_string(taxids)
	lingroup = convert_LIN_string(lingroup)
	LINgroup_taxids = taxids[0:len(lingroup)] #taxids of the lingroup
	#print(LINgroup_taxids)
	#print(len(lingroup))
	return LINgroup_taxids

def cumulative_sum(taxids, in_file):
	reads=0
	last_taxid = taxids[-1]
	#print(last_taxid)
	index = in_file[in_file[4] == int(last_taxid)].index.values
	if index.size >0:
		index = int(index)
		reads = in_file[1][index]
	#print(reads)
	return reads	
#	cumsum = 0
#	for i in range(len(taxids)):
#		#print(taxids[i])
#		index = in_file[in_file[4] == int(taxids[i])].index.values #index of match 
#		#print(index)
#		if index.size > 0:
#			index = int(index)
#			#print(index)
#			cumsum = cumsum + in_file[2][index]
#	#print(cumsum)
#	return cumsum
		
def assigned_reads(taxids, in_file):
	reads=0
	last_taxid = taxids[-1]
	#print(last_taxid)
	index = in_file[in_file[4] == int(last_taxid)].index.values
	if index.size >0:
		index = int(index)
		reads = in_file[2][index] 
	#print(reads)
	return reads

def total_reads_count(taxids,in_file):
	reads=0
	taxid = taxids[0] #taxid of the first tax rank; root of all rssc genomes
	#print(taxid)
	index = in_file[in_file[4] == int(taxid)].index.values
	#print(index)
	if index.size >0:
		index = int(index)
		reads = in_file[1][index]
	#print(reads)
	return reads

def total_reads_length(taxids, in_output):
	read_length=0
	last_taxid = taxids[-1]
	#print(last_taxid)
	index = in_output[in_output[2] == int(last_taxid)].index.values
	#print(index)
	if index.size >0:
		for i in range(len(index)):
			curr_index = int(index[i])
			if '|' in str(in_output[3][curr_index]): ####in case of paired reads eg: 151|149 use only first read length
				read_length = read_length + int(in_output[3][curr_index].split('|')[0])
			else:
				read_length = read_length + in_output[3][curr_index]
	#print(reads)
	return read_length

def  main():
	p = argparse.ArgumentParser()
	p.add_argument('--lin_file', help = 'txt file contaning lingroup names and prefixes')
	p.add_argument('--data_file', help = 'txt file containing the taxonom details produced in the db construction step')
	p.add_argument('--in_file_report', help = 'report output generated from kraken2 (condensed output file)')
	p.add_argument('--in_file_output', help = 'default output generated from kraken2 ( output file)')
	p.add_argument('--output')
	args = p.parse_args()

	lingroup_file = args.lin_file
	#reading the lin file
	lin_file = pd.read_csv(lingroup_file,sep='\t')
	
	data_file = args.data_file
        #reading the file      
	data = pd.read_csv(data_file,sep='\t')
	data['taxid_LIN'] = data['taxid_LIN'].str.replace("[\]\[]", '')
	data['parent_LIN'] = data['parent_LIN'].str.replace("[\]\[]", '')

	in_file = args.in_file_report
        #reading the file
	in_file = pd.read_csv(in_file,sep='\t',header=None,index_col=False)
	
	in_output = args.in_file_output
	#reading the file
	in_output = pd.read_csv(in_output,sep='\t',header=None,index_col=False)
	
	#open output file for report
	#output = open(args.output, 'w')
	out_file = pd.read_csv(lingroup_file,sep='\t')
	#out_file['LINgroup_Name'] = ''
	#out_file['LINgroup_prefix'] = ''
	out_file['Assigned_reads'] = ''
	out_file['Percentage_assigned_reads'] = ''
	out_file['Unique_Assigned_reads'] = ''
	out_file['Percentage_unique_assigned_reads'] = ''
	out_file['Total_reads_length'] = ''
	temp_taxid = find_taxid_of_lingroup(lin_file['LINgroup_prefix'][1], data) ##to find the first taxid of all
	#print(temp_taxid)
	total_reads=total_reads_count(temp_taxid, in_file)
	#print(total_reads)
	i=0
	while (i < len(lin_file['LINgroup_Name'])) and (total_reads is not 0) :
		#find list of taxids associated with best match of LINgroup
		taxid = find_taxid_of_lingroup(lin_file['LINgroup_prefix'][i], data)
		
		cumulative_reads = cumulative_sum(taxid, in_file)
		unique_reads = assigned_reads(taxid, in_file)
		reads_length = total_reads_length(taxid, in_output)
		#adding the result to the output file
		out_file['Assigned_reads'][i] = cumulative_reads
		out_file['Percentage_assigned_reads'][i] = (cumulative_reads/total_reads)*100
		out_file['Unique_Assigned_reads'][i] = unique_reads
		out_file['Percentage_unique_assigned_reads'][i] = (unique_reads/total_reads)*100
		out_file['Total_reads_length'][i] = reads_length
		i = i + 1

	#print(out_file)
	#out_file = open(out_file, 'w')
	#output = out_file.copy()
	df = pd.DataFrame({"LINgroup_Name":['Total_reads'], "Assigned_reads": [total_reads]})
	#out_file.append('LINgroup_Name': 'Total_reads', 'Cumulative_reads': str(in_file[1][1]))
	#print(out_file)
	out_file = out_file.append( df, ignore_index=True)
	print(out_file)
	out_file.to_csv(args.output, sep=',', index=False)	

if __name__=='__main__':
	main()



