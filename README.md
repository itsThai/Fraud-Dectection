Objective/n
This Final project demonstrates how we complete the Task 1 of the find it contest on the website findit.univ-lr.fr Task 1 requires us to do:
- Obtain the datasets from the website.
- Analyze the datasets the problem: In this case, to detect signs of forgery in a flow of document.
- Choose the correct methods to extract the forgery from images.
- Set a parameter of chosen methods.
- Analyze the results obtained from programs.

Methodology/n
From the sample, we could see that the receipts contain characters and digits that have similar fonts. Combined with large empty spaces present in the image, we could make a deduction that the forgery was created by manipulating the details on the receipt itself in order to make the forged receipt look more legitimate. For this reason, we will use the Copy-Move detection method written in "Detection of Copy-Move Forgery in Digital Images" [*] by Jan Lukás, Jessica Fridrich and David Soukai. After that, we will evaluate the results using the given Findit database.
- Step 1: we run a sliding window through the image, each time a sliding window passes through, we apply a DCT transformation on that portion of the image to create a DCT matrix.
- Step 2: We quantized that matrix by dividing every entry of the DCT matrix by a Quantization Matrix based on the quality factor. We use a modification of JPEG's Quantization Matrix.
Originally, JPEG standard had the Quantization Matrix size of 8x8, but because our window size is 16x16, and the Quantization Matrix must match the window size, we decided to use the one mentioned in the paper that we based our method on.
- Step 3: We take our Quantized Matrix, sort it in lexicographical order. This allows us to compare them more easily.
If two Quantized Matrices match, we take their upper left coordinates and accept the differences to get the shift vectors value.
- Step 4: Finally, we count the shift vectors with the same shift value and decide if the count surpasses the threshold defined in the program input, then we can determine the image has tampered.

Implement/n
Run format python3 robust.py <folderpath> <filecheck.xml> <windowsize> <Q-factor> <threshold> <numThreads>
In which we have:
- <folderpath> contains a path to the image folder.
- <filecheck.xml> is the Groundtruth file for checking progress in real time.
- <windowsize> is the size of window we need to extract from the image for copy detection. Although this option is made, no matter how you choose, it is hard-set to 16 in the code.
- <Q-factor> is the JPEG compression factor of the image.
- Threshold is the value you "feel" that the algorithm will work at maximum accuracy. Technically speaking, it is the value that if any counting of the shift vectors with the same shift value surpasses during scanning the image, we declare the image as being forged.
- <numThreads> is the number of threads used in the program for processing multiple images. We recommend you use 3 threads for machines with <= 8GB of RAM and 7 threads for machines with <= 16GB of RAM.

Tools being used/n
- Python v.3.9 with the installations of following packages:
- Opencv-python: For image processing.
- Scipy, numpy: For big arrays handling and useful & fast mathematical tools.
- BeautifulSoup4, lxml: For parsing xml data from the Groundtruth file to provide realtime accuracy statistics.
- Scikit-image: For extracting window in the image efficiently

Conclusion/n
The result table shows that the higher the threshold is, the more accurate we can detect the forgery. However, it is worth noting that many forged images got passed detection due to the massive drop in recall measurement while the precision is not increased drastically.
In specific threshold levels, we can also see that the implication of JPEG compression can help or reduce the accuracy. For example, if the threshold is 200 matches, the quality factor can cause the algorithm’s accuracy to go extremely low, about 0.2%. Meanwhile, the accuracy fluctuated wildly for a threshold of 500 matches but generally got better results with higher quality factors.
While implementing this method does not bring a high accuracy, we think that if
better development of the technique, combined with machine learning to fine-tune the threshold and quality factor and larger pool of samples to learn from, this method may later become a success. A practical tool to detect tampering.
