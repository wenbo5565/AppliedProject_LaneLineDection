# **Finding Lane Lines on the Road** 

## Project Overview

This is the first project in the Computer Vision section of Udacity's Self-Driving Car Engineer Course. In this project, I leverage several computer
vision techniques to detect the traffic lane lines given input images. The specific tasks are:

* Build a pipeline in Python to detect lane lines in images.
* Leverage the pipeline to detect lane lines in videos

The sample input image is:

<img src="./ExampleImage/solidWhiteRight.jpg" width="400">

The sample output image is:

<img src="./ExampleImage/solidWhiteRight-output.jpg" width="400">

## Project Details

### 1. Pipeline to Detect Traffic Lane Lines

Input image

<img src="./ExampleImage/original.png" width="450">


My pipeline consists of 5 steps. 

* Convert RGB image to grayscale 

<img src="./ExampleImage/gray.png" width="450">

* Detect edges in images by Canny edge dector

<img src="./ExampleImage/edge.png" width="450">

* Remove edges out of defined interest of areas

<img src="./ExampleImage/areaofinterest.png" width="450">

* Apply Hough transformation to detect lines in images (output endpoints of detected lines)

* Apply weighted regression to fit left and right lane lines

<img src="./ExampleImage/leftrightlane.png" width="450">

Output image by merging input image and detected lanes.

<img src="./ExampleImage/output.png" width="450">

### 2. Key Design and Implementation in the Pipeline

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...




### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
