#!/usr/bin/python

import os
import sys
import pickle


# get the nodeIndex
class NodeClass:
	pass
pklFile = open('nodeHistory_'+sys.argv[1]+'.pkl','rb')
nodeHistory = pickle.load(pklFile)
pklFile.close()
nodeNumber = str(nodeHistory[0].nodeIndex)
outputFile = 'Node_'+nodeNumber+'.avi'
fps = '12'
bitrate = '1800'
path ='./nodeHistory/'+nodeNumber+'/'
frameName=path+'Node_'+nodeNumber+'_*.png'
encodeCommand = 'mencoder mf://'+frameName+' -mf type=png:fps='+fps+' -ovc lavc -lavcopts vcodec=mpeg4:vbitrate='+bitrate+' -o '+outputFile
print encodeCommand
os.system(encodeCommand)
print 'Finished making video'

