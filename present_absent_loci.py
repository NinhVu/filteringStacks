#!/usr/bin/python3.4
# present_absent.py 3/12/16 by Ninh Vu
# This program will filter loci/stacks found in only individuals ask by user

import glob, sys, os
os.getcwd()

input_list = input("\nEnter individuals in catalog (uStacks id) you want to filter e.g. 106,121,112,120 : ")

# convert input list into list of integers and sort
user_list = input_list.split(",")
user_list = list(map(int, user_list))
user_list.sort()

print("\nOnly stacks with these individuals will be filtered:",user_list,"\n")
print("Takes a few seconds or minutes to filter depending on number of stacks/loci in catalog...")



# filter tags.tsv__________________________________________________________________________________________________________________________________________________
for file in glob.glob("*.tags.tsv"):	# open ***.catalog.tags.tsv file in current directory
    tags = open(file, 'r')
	
header = tags.readline()
data = tags.readline()
tags_tsv_loci=[]

while data:
    # split row into list and define variables for loop below
    catCount = 0
    rowItems = data.split("\t")

    # v2: split into oneList then create two lists: sampleID and catalogID. Convert both lists into integers, remove duplicate items and finally sort sampleID
    for y in rowItems:  # loop takes strings and convert into list of sample_catalogs
        if catCount == 8:
            samples_catalog = rowItems[8]
            oneList = samples_catalog.split(",") # e.g. ['27_22319', '28_874']
        catCount +=1
    sampleID = [i.split('_')[0] for i in oneList] # split oneList and make sample list. [0] represents the first item of split item.
    catalogID = [i.split('_')[1] for i in oneList] # split oneList and make catalog list. [1] represents the second item of the split item. Not necessary here.
    sampleID, catalogID = list(map(int, sampleID)), list(map(int, catalogID))
    sampleID = list(set(sampleID))  # REMOVE DUPLICATE B/C YOU WANT ALL STACKS EVEN ONES WITH MULTITPLE COPIES 
    sampleID.sort() # sort sampleID
    if sampleID == user_list:
        tags_tsv_loci.append(rowItems[2])

    # read next line
    data = tags.readline()

tags_tsv_loci = list(map(int, tags_tsv_loci))   # convert string list to int list
tags_tsv_loci = list(set(tags_tsv_loci))  		# remove duplicate items
tags_tsv_loci.sort()	# sort loci
tags.close()


# create whitelist.txt_____________________________________________________________________________________________________________________________________________
whitelist = open('present_absent_whitelist.txt', 'w')
whitelist.write('\n'.join('%s' % x for x in tags_tsv_loci))	# write whitelist with only locus
whitelist.write('\n')
print("\n\nYour present/absent stacks of whitelist file present_absent_whitelist.txt is ready.\n\n\n")

whitelist.close()
