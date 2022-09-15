import cv2
import sys
import numpy as np
import threading
from os import listdir, makedirs, remove, system
from os.path import isfile, join, islink, isdir, exists
from shutil import rmtree
from bs4 import BeautifulSoup as bs
from scipy import fftpack
from concurrent.futures import ThreadPoolExecutor
from skimage.util import view_as_windows

if len(sys.argv) <= 6:
    print("[Usage]: \n\tpython3 robust.py <folderpath> <filecheck.xml> <windowsize> <Q-factor> <threshold> <numThreads>")
    exit(-1)

"""

"""
def createCleanFolder(foldername):
    if not exists(foldername):
        makedirs(foldername)
    else:
        for filename in listdir(foldername):
            file_path = join(foldername, filename)
            try:
                if isfile(file_path):
                    remove(file_path)
                elif isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

createCleanFolder(".tmp")

# Input arguments from the cmd line
folderimgpath       = sys.argv[1]       # Folder path
groundtruthfilename = sys.argv[2]       # Groundtruth file input
window_size         = 16                # Get window size
qfactor             = int(sys.argv[4])  # Q-factor number input
threshold_count     = int(sys.argv[5])  # Threshold defined for the program
maxThreadNo         = int(sys.argv[6])  # More thread, for more power!

# Keep track of process
true_output  = 0
total_output = 0

# Get groundtruth file
groundtruthfile = open(groundtruthfilename, "r")
checker = bs("".join(groundtruthfile.readlines()), "lxml")

"""
    dct(), idct():
        Discrete cosine transform and its version of inverse.
"""
dct  = lambda x: fftpack.dct(x, norm='ortho')
idct = lambda x: fftpack.idct(x, norm='ortho')

"""

"""
def getQuantizationMatrix(q):
    # Define default matrix
    Q8 = np.array(
        [[16,11,10,16,24,40,51,61],
         [12,12,14,19,26,58,60,55],
         [14,13,16,24,40,57,69,56],
         [14,17,22,29,51,87,80,62],
         [18,22,37,56,68,109,103,77],
         [24,35,55,64,81,104,113,92],
         [49,64,78,87,103,121,120,101],
         [72,92,95,98,112,100,103,99]]
    )

    # Calculate S
    if q < 50:
        S = 5000 / q
    else:
        S = 200 - 2*q

    # Loop to convert basic matrix used in JPEG to one that coresponds to image quality
    for i in range(8):
        for j in range(8):
            Q8[i, j] = int((S * Q8[i, j] + 50) / 100.0)

    # Prevents divide by 0 during quantization
    Q8[Q8 == 0] = 1

    # Create an empty array 16x16
    Q16 = np.empty([16, 16])

    # Fill
    Q16[0:8,  0:8 ] = Q8 * 2.5
    Q16[8:16, 0:8 ] = 2.5 * Q8[7, 0] * np.ones([8, 8])
    Q16[0:8,  8:16] = 2.5 * Q8[0, 7] * np.ones([8, 8])
    Q16[8:16, 8:16] = 2.5 * Q8[7, 7] * np.ones([8, 8])

    # Formula specify
    Q16[0, 0] *= 0.8

    return Q16
Q = getQuantizationMatrix(qfactor)

"""

"""
def getShiftVector(x1, y1, x2, y2):
    if y1 > y2:
        return (y1-y2, x1-x2)
    else:
        return (y2-y1, x2-x1)

"""

"""
def processImage(filename):
    print("Checking {}...".format(filename))


    # Get image
    print("Get image...")
    img = cv2.imread(join(folderimgpath, filename), cv2.IMREAD_GRAYSCALE)
    if str(type(img)) == "<class 'NoneType'>":
        return



    # Set variables for pre-computing
    X_winSize = img.shape[1] // 4 - window_size + 1



    # Resize images
    img_resize_shifted = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) - 128



    # Slide along window
    print("Get slide vectors...")
    windows = view_as_windows(img_resize_shifted, (window_size, window_size))



    # Calculate DCT...
    print("Calculating DCT...")
    dcts = (dct(windows).reshape(-1, window_size, window_size) / Q).reshape(-1, window_size * window_size).astype(int)



    # Sort array in lexalonlon order
    print("Sorting {} elements...".format(len(dcts)))
    index = np.lexsort(np.rot90(dcts))



    # Check for subsequence stuffs...
    print("Count...")
    count    = {}
    detected = 0
    for i_index in np.arange(len(index) - 1):


        # Calculate shift vector
        shift_vec = getShiftVector(
            index[i_index]   % X_winSize, index[i_index]   // X_winSize,
            index[i_index+1] % X_winSize, index[i_index+1] // X_winSize
        )



        # Skip if vector shifted is too small...
        if abs(shift_vec[0]) <= window_size and abs(shift_vec[1]) <= window_size:
            continue


        # Compares if the DCT coefficients matchup
        if (dcts[index[i_index]] == dcts[index[i_index+1]]).all():

            # Add to dictionary
            if shift_vec not in count:
                count[shift_vec] = 1
            else:
                count[shift_vec] += 1

            # Compare with threshold count...
            if count[shift_vec] > threshold_count:
                detected = 1
                break



    # Upgrade progress..
    print("Update output values...")
    global true_output
    global total_output
    actual_result = int(checker.find("doc", {"id" : filename.split('.')[0]})["modified"])
    if actual_result == detected:
        true_output += 1
    total_output += 1



    # Print true
    print("{}% true: {}/{}".format(true_output * 100.0 / total_output, true_output, total_output))



    # Write to tmp file
    print("Write to tmp file...")
    tmp_outputfile = open(".tmp/" + str(threading.current_thread().native_id), 'a+')
    tmp_outputfile.write('<doc id="{}" modified="{}"/>\n'.format(filename.split('.')[0], detected))
    tmp_outputfile.close()



# For each file in folder, process image (now with multiple threads yey yey)
executor = ThreadPoolExecutor(max_workers=maxThreadNo)
for filename in listdir(folderimgpath):
    if isfile(join(folderimgpath, filename)):
        executor.submit(processImage, filename)


# Wait for data to finish writing to file
print("Wait for all threads to finish...")
executor.shutdown(wait=True)



# Output file creation
print("Write all data to output file...")
outputfilename = "output_q{}_t{}.xml".format(qfactor, threshold_count)
outputfile     = open(outputfilename, 'w')
outputfile.write("<?xml version='1.0' encoding='utf-8'?>\n<GT>\n")



# Append all data to a single output file.
for filename in listdir(".tmp"):
    file_path = join(".tmp", filename)
    try:
        if isfile(file_path):
            tmpfile = open(file_path, 'r')
            outputfile.write(tmpfile.read())
            tmpfile.close()
    except Exception as e:
        print('Failed to write {}. Reason: {}'.format(file_path, e))



# Write end data to file.
outputfile.write("</GT>")
outputfile.close()



# Executes Grouthtruth file evaluation
# print("Evaluate file...")
# evalfilename = "output_q{}_t{}.csv".format(qfactor, threshold_count)
# system("python .\EvalT1.py -fg T1-GT.xml -fe {} -o {}".format(outputfilename, evalfilename))
