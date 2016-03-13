#!/usr/bin/python3
# filtering_cStacks_v1.py 3/12/16 by Ninh Vu
# This program will filter out four categories of undesirable loci and/or SNPs: (1) loci not found in sample list of filter catalog.tag.tsv,
# (2) loci with more than two alleles (3) loci with more than four SNPs and (4) SNPs found between position 1 to 24 and/or 75 or greater of sequence.
# to run this program on server simply type in the program name
# you need three input files in current/working directory e.g. batch_1.catalog.tags.tsv, batch_1.catalog.snps.tsv and batch_1.catalog.alleles.tsv

import glob, sys, os
os.getcwd()

print("\n\n\n\n*************************************************************************************************************************************************\n")
print("This program will filter out four categories of undesirable loci and/or SNPs from cStacks output files:\n")
print("(1) loci not found in sample list of filtered catalog.tags.tsv \n")
print("(2) loci with more than two alleles\n")
print("(3) loci with more than the user input number of SNPs and \n")
print("(4) SNPs found between position 6 to 24 and/or 75 or greater of sequence.\n")
print("****Filter 1 in more detail explanation********")
print("Only individuals (uStacks id) you enter get filter. For example if you enter 112, 106, 121 and 120, ONLY stacks with these individuals get filter.")
print("Below are a few examples of NONfiltered stacks.\n")
print("1610:  106_2345, 112_5674, 120_21345, 120_22345         - stack 1610 has four stacks but two are found in individual 120.")
print("110:   106_999, 112_96744, 120_145, 120_2345, 121_24500 - stack 110 has five stacks but two are found in individual 120.")
print("13666: 106_7999, 112_44587, 120_786                     - stack 13666 is found in only three individauls.\n")
print("This prevents choosing stacks with MULTIPLE COPIES from one individual, or stacks NOT in majority of individuals in poputlation(s).\n\n")

input_list = input("\nEnter individuals in catalog (uStacks id) you want to filter e.g. 106,121,112,120 : ")
max_number_of_SNPs = input("\nEnter the maximum number of SNPs per locus you want to see in a stack: ") 

# convert input list into list of integers and sort
user_list = input_list.split(",")
user_list = list(map(int, user_list))
user_list.sort()
max_number_of_SNPs = int(max_number_of_SNPs)

print("\nOnly stacks with these individuals will be filtered:",user_list,"However, stacks with more than",max_number_of_SNPs,"SNPs will be excluded.\n")
print("Takes a few seconds or minutes to filter depending on number of stacks/loci in catalog...")

# filter tags.tsv__________________________________________________________________________________________________________________________________________________
for file in glob.glob("*tags.tsv"):	# open ***.catalog.tags.tsv file in current directory
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
    # sampleID = list(set(sampleID))  # remove duplicate items 
    sampleID.sort() # sort sampleID
    if sampleID == user_list:
        tags_tsv_loci.append(rowItems[2])

    # read next line
    data = tags.readline()

tags_tsv_loci = list(map(int, tags_tsv_loci))   # convert string list to int list
tags_tsv_loci = list(set(tags_tsv_loci))  		# remove duplicate items
tags.close()


# filter alleles.tsv_______________________________________________________________________________________________________________________________________________
for file in glob.glob("*alleles.tsv"):
    alleles = open(file, 'r')

header = alleles.readline()
alleles_data = alleles.readline()
alleles_tsv_loci=[]

while alleles_data:
    # split row into list and define variables for loop below
	alleles_rowItems = alleles_data.split("\t")
	
	if len(alleles_rowItems[3]) <= max_number_of_SNPs:	# exlcude markers with more than asked input
		alleles_tsv_loci.append(alleles_rowItems[2])
	alleles_data = alleles.readline()	# read next line

alleles_tsv_loci = list(set(alleles_tsv_loci)) 		# remove duplicate items
alleles_tsv_loci = list(map(int, alleles_tsv_loci))	# convert list of strings to list of integers
alleles.close()


# filter snps.tsv__________________________________________________________________________________________________________________________________________________
for file in glob.glob("*snps.tsv"):
	snps = open(file, 'r')

header = snps.readline()
snps_data = snps.readline()
snps_tsv_loci, snps_tsv_pos=[],[]
snps_pos=0
while snps_data:
	# split row into list and define variables for loop below
	snps_rowItems = snps_data.split("\t")
	snps_pos = int(snps_rowItems[3])

	if snps_pos >=25 and snps_pos <=75 and snps_rowItems[8] == '-':	# exclude SNPs with more than 2 alleles, below 25 bp and above 75 bp (for longer reads)
		snps_tsv_loci.append(snps_rowItems[2])
		snps_tsv_pos.append(snps_rowItems[3])
	snps_data = snps.readline()	# read next line

snps_tsv_loci = list(map(int, snps_tsv_loci))	# convert list of strings to list of integers
snps_tsv_pos = list(map(int, snps_tsv_pos))		# convert list of strings to list of integers
snps.close()


# filter to create 1st_filter_cStacks_whitelist.txt________________________________________________________________________________________________________________
whitelist = open('1st_filter_cStacks_whitelist.txt', 'w')
snpsZip = zip(snps_tsv_loci,snps_tsv_pos)	# zip locus and snp_pos creating tuple from snps.tsv filter

SnpsTags = [tup for tup in snpsZip if tup[0] in tags_tsv_loci]	# create new tuple with only loci found in tags_tsv_loci filter
SnpsTagsAlleles = [tup for tup in SnpsTags if tup[0] in alleles_tsv_loci] # create yet newer tuple with only loci found in alleles_tsv_loci filter

whitelist.write('\n'.join('%s\t%s' % x for x in SnpsTagsAlleles))	# write tab delimited whitelist file
whitelist.write('\n')
print("\n\nYour filtered whitelist file 1st_filter_cStacks_whitelist.txt is ready.\n\n\n")

whitelist.close()





