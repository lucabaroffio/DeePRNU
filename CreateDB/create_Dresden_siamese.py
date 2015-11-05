import cv2
import cv
import glob
import os
import random
import sys


WINSIZE = 52 # window size
NUMPAIRS = 100000 # number of training pairs
POSRATIO = 0.5 # ratio of positive samples, P/(P + N)
TOUGHRATIO = 0.5 # ratio of tough non-matching pairs, i.e. patches from the same image
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
			break
	# print filename	
	# print curCam
	assert(curCam!=None)
	matching = [s for s in filelist if ((curCam in s) & (s!=filename))]
	# matching = [x for x in xrange(0, len(filelist)) if ((curCam in filelist[x]) & (filelist[x]!=filename))]
	return matching

def getCamera(filename):
	
	curCam = None
	with open(CAMERAFILE) as f:
		cameras = f.read().splitlines()
	for c in cameras:
		if (filename.find(c)>0):
			curCam = c
			break
	# print filename	
	# print curCam
	assert(curCam!=None)
	return curCam


def main():

	random.seed(666)
	assert (not os.path.exists('patches'))

	os.makedirs('patches')
	os.makedirs('patches/1')
	os.makedirs('patches/2')

	filelist = glob.glob(os.path.join(DATAPATH, '*.JPG'))

	numPos = int(POSRATIO*NUMPAIRS)
	numNeg = int(NUMPAIRS - numPos)
	numTough = int(numNeg*TOUGHRATIO)

	f1 = open('patches/1/fileList.txt', 'w')
	f2 = open('patches/2/fileList.txt', 'w') 

	# positive pairs
	print 'creating positive pairs...'
	for x in xrange(numPos):
		drawProgressBar(float(x)/numPos)
		while(1):
			im1Path = random.choice(filelist) # open a random image
			im1 = cv2.imread(im1Path)
			if ((im1.shape[0]>WINSIZE) and (im1.shape[1]>WINSIZE)):
				break
			print 'invalid image: ' + im1Path

		nRows = im1.shape[0]
		nCols = im1.shape[1]
		nWindRows = int((nRows - WINSIZE)/WINSIZE) # get the number of hor and vert windows
		nWindCols = int((nCols - WINSIZE)/WINSIZE) 
		curWind = [random.choice(xrange(nWindRows)), random.choice(xrange(nWindCols))] # random window
		wind1 = im1[curWind[0]*WINSIZE:(curWind[0]*WINSIZE + WINSIZE), curWind[1]*WINSIZE:(curWind[1]*WINSIZE + WINSIZE), :]
		assert((wind1.shape[0] == WINSIZE) & (wind1.shape[1] == WINSIZE))
		

		# get a matching window
		while(1):
			im2Path = random.choice(getMatchingImagesPath(im1Path, filelist))
			im2 = cv2.imread(im2Path)
			if ((im1.shape[0]>WINSIZE) and (im1.shape[1]>WINSIZE)):
				break
			print 'invalid image: ' + im2Path

		wind2 = im2[curWind[0]*WINSIZE:(curWind[0]*WINSIZE + WINSIZE), curWind[1]*WINSIZE:(curWind[1]*WINSIZE + WINSIZE), :]
		if not((wind2.shape[0] == WINSIZE) & (wind2.shape[1] == WINSIZE)):
			continue

		cv2.imwrite(os.path.join('patches', '1', ("%08d" % (2*x)) + '.jpg'), wind1, [cv.CV_IMWRITE_JPEG_QUALITY, 100])

		cv2.imwrite(os.path.join('patches', '2', ("%08d" % (2*x)) + '.jpg'), wind2, [cv.CV_IMWRITE_JPEG_QUALITY, 100])

		f1.write(os.path.join('patches', '1', ("%08d" % (2*x)) + '.jpg') + ' 1\n')
		f2.write(os.path.join('patches', '2', ("%08d" % (2*x)) + '.jpg') + ' 1\n')
	
	drawProgressBar(1.0)

	print 'creating negative pairs...'
	for x in xrange(numNeg):
		drawProgressBar(float(x)/numNeg)
		while(1):
			im1Path = random.choice(filelist) # open a random image
			im1 = cv2.imread(im1Path)
			if ((im1.shape[0]>WINSIZE) and (im1.shape[1]>WINSIZE)):
				break
			print 'invalid image: ' + im1Path

		nRows = im1.shape[0]
		nCols = im1.shape[1]
		nWindRows = int((nRows - WINSIZE)/WINSIZE) # get the number of hor and vert windows
		nWindCols = int((nCols - WINSIZE)/WINSIZE) 
		curWind = [random.choice(xrange(nWindRows)), random.choice(xrange(nWindCols))] # random window
		wind1 = im1[curWind[0]*WINSIZE:(curWind[0]*WINSIZE + WINSIZE), curWind[1]*WINSIZE:(curWind[1]*WINSIZE + WINSIZE), :]
		assert((wind1.shape[0] == WINSIZE) & (wind1.shape[1] == WINSIZE))
		

		# get a non-matching window
		if (x < numTough):
			im2 = im1
		else:
			while(1):
				im2Path = random.choice(filelist)
				if (getCamera(im2Path) != getCamera(im1Path)):
					im2 = cv2.imread(im2Path)
					if ((im2.shape[0]>WINSIZE) and (im2.shape[1]>WINSIZE)):
						break
					print 'invalid image: ' + im2Path

		nRows = im2.shape[0]
		nCols = im2.shape[1]
		nWindRows = int((nRows - WINSIZE)/WINSIZE) # get the number of hor and vert windows
		nWindCols = int((nCols - WINSIZE)/WINSIZE) 
		while(1):
			curWind2 = [random.choice(xrange(nWindRows)), random.choice(xrange(nWindCols))] # random window
			if ((curWind2[0] != curWind[0]) and (curWind2[0] != curWind[0])):
				break

		wind2 = im2[curWind2[0]*WINSIZE:(curWind2[0]*WINSIZE + WINSIZE), curWind2[1]*WINSIZE:(curWind2[1]*WINSIZE + WINSIZE), :]
		assert((wind2.shape[0] == WINSIZE) & (wind2.shape[1] == WINSIZE))

		cv2.imwrite(os.path.join('patches', '1', ("%08d" % (2*x + 1)) + '.jpg'), wind1, [cv.CV_IMWRITE_JPEG_QUALITY, 100])

		cv2.imwrite(os.path.join('patches', '2', ("%08d" % (2*x + 1)) + '.jpg'), wind2, [cv.CV_IMWRITE_JPEG_QUALITY, 100])

		f1.write(os.path.join('patches', '1', ("%08d" % (2*x + 1)) + '.jpg') + ' 0\n')
		f2.write(os.path.join('patches', '2', ("%08d" % (2*x + 1)) + '.jpg') + ' 0\n')
	
	drawProgressBar(1.0)
	f1.close()
	f2.close()

		
		


if __name__ == "__main__":
	main()

















    

	
	
	







