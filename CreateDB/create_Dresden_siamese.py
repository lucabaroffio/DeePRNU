import cv2
import cv
import glob
import os
import random
import sys


WINSIZE = 52 # window size
NUMPAIRS = 100 # number of training pairs
POSRATIO = 0.5 # ratio of positive samples, P/(P + N)
DATAPATH = '/data/dataset/Dresden/natural'
CAMERAFILE = 'Dresden_cameraList'

def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


def getMatchingImagesPath(filename, filelist):
	
	curCam = None
	with open(CAMERAFILE) as f:
		cameras = f.read().splitlines()
	for c in cameras:
		if (filename.find(c)>0):
			curCam = c
	# print filename	
	# print curCam
	assert(curCam!=None)
	matching = [s for s in filelist if ((curCam in s) & (s!=filename))]
	# matching = [x for x in xrange(0, len(filelist)) if ((curCam in filelist[x]) & (filelist[x]!=filename))]
	return matching


def main():

	random.seed(666)
	assert (not os.path.exists('matching'))
	assert (not os.path.exists('non-matching'))

	os.makedirs('matching')
	os.makedirs('matching/1')
	os.makedirs('matching/2')

	filelist = glob.glob(os.path.join(DATAPATH, '*.JPG'))

	numPos = int(POSRATIO*NUMPAIRS)
	numNeg = int(NUMPAIRS - numPos)

	# positive pairs
	print 'creating positive pairs...'
	for x in xrange(numPos):
		drawProgressBar(float(x)/numPos)
		im1Path = random.choice(filelist) # open a random image
		im1 = cv2.imread(im1Path)
		nRows = im1.shape[0]
		nCols = im1.shape[1]
		nWindRows = int((nRows - WINSIZE)/WINSIZE) # get the number of hor and vert windows
		nWindCols = int((nCols - WINSIZE)/WINSIZE) 
		curWind = [random.choice(xrange(nWindRows)), random.choice(xrange(nWindCols))] # random window
		wind1 = im1[curWind[0]*WINSIZE:(curWind[0]*WINSIZE + WINSIZE), curWind[1]*WINSIZE:(curWind[1]*WINSIZE + WINSIZE), :]
		assert((wind1.shape[0] == WINSIZE) & (wind1.shape[1] == WINSIZE))
		

		# get a matching window
		im2Path = random.choice(getMatchingImagesPath(im1Path, filelist))
		im2 = cv2.imread(im2Path)
		wind2 = im2[curWind[0]*WINSIZE:(curWind[0]*WINSIZE + WINSIZE), curWind[1]*WINSIZE:(curWind[1]*WINSIZE + WINSIZE), :]
		assert((wind2.shape[0] == WINSIZE) & (wind2.shape[1] == WINSIZE))

		cv2.imwrite(os.path.join('matching', '1', ("%08d" % x) + '.jpg'), wind1, [cv.CV_IMWRITE_JPEG_QUALITY, 100])

		cv2.imwrite(os.path.join('matching', '2', ("%08d" % x) + '.jpg'), wind2, [cv.CV_IMWRITE_JPEG_QUALITY, 100])
	
	drawProgressBar(1.0)

		
		


if __name__ == "__main__":
	main()

















    

	
	
	







