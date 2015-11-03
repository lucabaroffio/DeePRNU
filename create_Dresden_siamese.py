import cv2
import glob
import os


WINSIZE = 52 # window size
NUMPAIRS = 100 # number of training pairs
POSRATIO = 0.5 # ratio of positive samples, P/(P + N)
DATAPATH = '/data/dataset/Dresden/natural'

asd = glob.glob(os.path.join(DATAPATH, '*.JPG'))

numPos = POSRATIO*NUMPAIRS
numNeg = NUMPAIRS - numPos

# positive pairs

print asd[2]











