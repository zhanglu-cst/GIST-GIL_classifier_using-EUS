## GIST-GIL_classifier_using-EUS

An deep learning-based GIST/GIL classifier using EUS. This classifer is shared for researching and learning only not for commercial use. We own the copyrights of this software. The classifier is developped using EUS images by UM-DP12-25R, and UM-DP20-25R (Olympus, Tokyo, Japan). According to our research, the classifier is only suitable for these EUS probes.


How to use the classifier:

1. The classifer can run on workstastion with Windows 10, 64 bit system. Deep learning environment is required. Python 3.7, CUDA 10.2, PyTorch(1.4.0+cpu), torchvision(0.5.0+cpu) should be correctly installed in your workstation.
2. Download the classifier.
3. Build a folder named "imageX" under C:\ .
4. Run run.py in cmd.
5. Open ultrasound_client.exe.
6. Frame ROI in EUS images to classify GISTs or GILs.