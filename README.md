<h2>Objective</h2>

<p>This Final project demonstrates how we complete the Task 1 of the find it contest on the website <strong>findit.univ-lr.fr.</strong> <br>
Task 1 requires us to do:</p>
<ul>
  <li>Obtain the datasets from the website.</li>
  <li>Analyze the datasets the problem: In this case, to detect signs of forgery in a flow of document.</li>
  <li>Choose the correct methods to extract the forgery from images.</li>
  <li>Set a parameter of chosen methods.</li>
  <li>Analyze the results obtained from programs.</li>
</ul>
  
<h2>Methodology</h2>
<p>From the sample, we could see that the receipts contain characters and digits that have similar fonts. Combined with large empty spaces present in the image, we could make a deduction that the forgery was created by manipulating the details on the receipt itself in order to make the forged receipt look more legitimate. For this reason, we will use the Copy-Move detection method written in <strong>"Detection of Copy-Move Forgery in Digital Images"</strong> by Jan Lukás, Jessica Fridrich and David Soukai. After that, we will evaluate the results using the given Findit database.</p>
<ol>
  <li>We run a sliding window through the image, each time a sliding window passes through, we apply a DCT transformation on that portion of the image to create a DCT matrix.</li>
  <li>We quantized that matrix by dividing every entry of the DCT matrix by a Quantization Matrix based on the quality factor. We use a modification of JPEG's Quantization Matrix.</li>
Originally, JPEG standard had the Quantization Matrix size of 8x8, but because our window size is 16x16, and the Quantization Matrix must match the window size, we decided to use the one mentioned in the paper that we based our method on.</li>
  <li>We take our Quantized Matrix, sort it in lexicographical order. This allows us to compare them more easily.
If two Quantized Matrices match, we take their upper left coordinates and accept the differences to get the shift vectors value.</li>
  <li>Finally, we count the shift vectors with the same shift value and decide if the count surpasses the threshold defined in the program input, then we can determine the image has tampered.</li>
</ol>
  
<h2>Implement</h2>
Run format <strong>python3 robust.py &lt; folderpath> &lt; filecheck.xml> &lt; windowsize> &lt; Q-factor>  &lt;threshold> &lt; numThreads></strong> <br>
In which we have:
<ul>
  <li>&lt;folderpath> contains a path to the image folder.</li>
  <li>&lt;filecheck.xml> is the Groundtruth file for checking progress in real time.</li>
  <li>&lt;windowsize> is the size of window we need to extract from the image for copy detection. Although this option is made, no matter how you choose, it is hard-set to 16 in the code.</li>
  <li>&lt;Q-factor> is the JPEG compression factor of the image.</li>
  <li>&lt;Threshold> is the value you "feel" that the algorithm will work at maximum accuracy. Technically speaking, it is the value that if any counting of the shift vectors with the same shift value surpasses during scanning the image, we declare the image as being forged.</li>
  <li>&lt;numThreads> is the number of threads used in the program for processing multiple images. We recommend you use 3 threads for machines with <= 8GB of RAM and 7 threads for machines with <= 16GB of RAM.</li>
</ul>
<h3>Tools being used</h3>
<ul>
  <li><strong>Python v.3.9</strong> with the installations of following packages:</li>
  <li><strong>Opencv-python</strong>: For image processing.</li>
  <li><strong>Scipy, numpy</strong>: For big arrays handling and useful & fast mathematical tools.</li>
  <li><strong>BeautifulSoup4, lxml</strong>: For parsing xml data from the Groundtruth file to provide realtime accuracy statistics.</li>
  <li><strong>Scikit-image</strong>: For extracting window in the image efficiently.</li>
  </ul>
  
<h2>Conclusion</h2>
The result table shows that the higher the threshold is, the more accurate we can detect the forgery. However, it is worth noting that many forged images got passed detection due to the massive drop in recall measurement while the precision is not increased drastically.
In specific threshold levels, we can also see that the implication of JPEG compression can help or reduce the accuracy. For example, if the threshold is 200 matches, the quality factor can cause the algorithm’s accuracy to go extremely low, about 0.2%. Meanwhile, the accuracy fluctuated wildly for a threshold of 500 matches but generally got better results with higher quality factors.
While implementing this method does not bring a high accuracy, we think that if
better development of the technique, combined with machine learning to fine-tune the threshold and quality factor and larger pool of samples to learn from, this method may later become a success. A practical tool to detect tampering.
