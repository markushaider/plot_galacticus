#!/usr/bin/python

import os

haloNumber = '78289'

outputFile = 'Node_'+haloNumber+'.avi'
fps = '12'
bitrate = '1800'
path ='./nodeHistory/'+haloNumber+'/'
frameName=path+'Node_'+haloNumber+'_*.png'

encodeCommand = 'mencoder mf://'+frameName+' -mf type=png:fps='+fps+' -ovc lavc -lavcopts vcodec=mpeg4:vbitrate='+bitrate+' -o '+outputFile
print encodeCommand
os.system(encodeCommand)
print 'Finished making video'
