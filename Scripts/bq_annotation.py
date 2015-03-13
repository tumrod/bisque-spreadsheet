#############################################################################
## LungMap Tags Annotation on Bisque                                       ##
## Edited 2: December 15, 2014                                             ##
## Last Edited: January 13, 2015                                           ##
## Multiple images annotations from tab delimited file                     ##
#############################################################################


##############################################################################
## Generating a list of annotations from file                               ##
## The file must be tab-delimited txt file                                  ##
##                                                                          ##
##############################################################################
def getList():
    totalList = []
    annotationList = []
    
    # open file
    # need to change file input to be parameter
    fileName = raw_input("Enter annotation file directory: ")
    #fileName = "/Users/tumrod/Documents/TACC/GenePaint/output/completeAnnotation.txt"
    for line in open(fileName):
        annotationList = []
        for item in line.split("\t"):
            if "\r" in item:
                index = item.index("\r")
                annotationList.append(item[:index])
                totalList.append(annotationList)
                annotationList = []
                annotationList.append(item[index:])
            else:
                annotationList.append(item)
    totalList.append(annotationList)
    return totalList

###############################################################################
## getFileName() parameters                                                  ##
##               - theList, can be from getList() or list of filenames,      ##
##               which has matched names with filenames on bisque images     ##
##               - index, the index of the names or filenames                ##
##               - word, additional string,                                  ##
##               which can be the file extension, for example, ".jpg"        ##
###############################################################################
def getFileName(theList,index, word):
    names = []
    for i in range(len(theList)):
        names.append(theList[i][index]+word)
    return names

###############################################################################
## Annotate images from the annotation/tags list                             ##
##                                                                           ##
###############################################################################

import getpass
import logging
import datetime
from bqapi import BQSession

#HOST= raw_input("host: ")
# default: "http://bovary.iplantcollaborative.org/" for iplant bisque

HOST="http://bovary.iplantcollaborative.org/"

# get username
USER= raw_input("user: ")
#USER= "<USERNAME>" 	#for static username

# get password
PASS= getpass.getpass()

timestamp = datetime.datetime.now().strftime("%I:%M-%m-%d-%Y")

#  authenticate a CAS session
logging.basicConfig (level = logging.DEBUG)

# unccomment to keep the log file
# logging.basicConfig(filename = timestamp + '.log', filemode = 'w', level = logging.DEBUG)
sess  = BQSession()
sess.init_cas(USER, PASS, bisque_root = HOST, create_mex = False)

# get the list of file names
theList = getList()
#print theList[0]
nameList = getFileName(theList, 0,"")
# ex. filename: Asrgl1_Lung.png 
#     official gene symbol: Arsgl1 in index = 2

# go through each image and add annotations for that image from annotation spreadsheet

#print sess.fetchxml('/data/dataset')
for i in range(len(nameList)):
    #for k in range(len(theList[0])):
            #tag = image.addTag(theList[0][k], theList[i][k])
            #tag = theList[0][k] +" =\t"+ theList[i][k]
            #print tag
    
    images = sess.query ('image', tag_query="filename:"+nameList[i])
    
    for image in images:
        # print image
        sess.clearTags(image.addTag(image.name))
        tag = image.addTag("filename", image.name)
        sess.save(tag)
        tag = image.addTag("upload_datetime", image.ts)
        sess.save(tag)
        tag = image.addTag("lastUpdate", timestamp)
        sess.save(tag)

        for k in range(1, len(theList[0])):
            tag = image.addTag(theList[0][k], theList[i][k])
            sess.save(tag)
    

