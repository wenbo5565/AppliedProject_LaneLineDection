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

Original image

<img src="./ExampleImage/original.png" width="400">


My pipeline consists of 5 steps. 

* Convert RGB image to grayscale 

<img src="./ExampleImage/gray.png" width="400">

* Detect edges in images by Canny edge dector

<img src="./ExampleImage/edge.png" width="500">

* Remove edges out of defined interest of areas
* Apply Hough transformation to detect lines in images
* Apply weighted regression to detect/draw left and right lane lines

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
