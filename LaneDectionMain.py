"""
This file creates a pipeline to input image files, do transformations and output image files with 
Lane imposed in the images.
"""

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os


# ==========================================================
# Define functions to process image.
#   Grayscale, Canny Edge Detection and Hough Trnasformation
# ==========================================================

def input_image(img_file):
    """ load an image file into python
        return an image array
    """
    return mpimg.imread(img_file)

def grayscale(img):
    """ apply grayscale transform 
        
        return image with only one channel
    """
    return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

def canny(img,low_threshold,high_threshold):
    """ apply canny edge dector to find edges
       
        return image array
    """
    return cv2.Canny(img,low_threshold,high_threshold)

def region_of_interest(img,vertices):
    """ apply a mask to an image to keep only pixels at interested locations.
        Interested areas are defined by vertices of polygon
        
        The input image is one channel (after grayscale transformation)
        
        vertices is a numpy array of vertices position
        
    """
    # a black image
    mask = np.zeros_like(img) 
    
    # set pixel value for within region of interest locations
    ignore_mask_color = 255 
    
    # filling pixels value inside polygon defined by "vertices"
    cv2.fillPoly(mask,vertices,ignore_mask_color)
    
    # returning  the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img,mask)
    return masked_image

def draw_lines(img,lines,color=[255,0,0],thickness=8):
    """ draw lines """
    
    """extrapolate  
       1. use sign of derivatives to separate left boundary points and right boundary points
       2. for each boundary, leverage linear regression to find boundary lines
    """
    
    left_x = [] # list for x coordinate of left boundary
    left_y = [] # list for y coordiante of left boundary
    right_x = []
    right_y = []
    
    # separate points to left or right boundary
    for line in lines:
        for x1,y1,x2,y2 in line:
            if (y2-y1)/(x2-x1)<0:
                left_x.extend([x1,x2])
                left_y.extend([y1,y2])
            elif (y2-y1)/(x2-x1)>0 and (y2-y1)/(x2-x1)<0.8: # horizontal line cannot be lane
                right_x.extend([x1,x2])
                right_y.extend([y1,y2])
            
    # fit regression line and output line parameters
    
    """
    The weights below is created for building a robust lane detector
    
    Both weights are based on the x coordinate of a point from Hough Transform.
    
    For right lane, the larger the x coordinate, the larger the weight is.
    For left lane, the larger the x coordinate, the smaller the weight is.
    """
    weights_right = np.square(right_x)/np.sum(np.square(right_x))
    weights_left = 1.0/np.array(left_x)/np.sum(1.0/np.array(left_x))
    
    # fit weighted linear regression
    z_left = np.polyfit(left_y,left_x,1,w=weights_left) # set y as known to predict x because position of bottom y is always the bottom of image
    z_right = np.polyfit(right_y,right_x,1,w=weights_right)
    f_left = np.poly1d(z_left)
    f_right = np.poly1d(z_right)
    
    # write left boundary
    y_bottom = img.shape[0] # maxmimum y value (the bottom of image)
    
    y_left_top = 325
    x_left_top = int(f_left(y_left_top))
    x_left_bottom = int(f_left(y_bottom)) # predict x coordiate for bottom ending points on the left bound
    cv2.line(img,(x_left_bottom,y_bottom),(x_left_top,y_left_top),color,thickness)
    
    # write right boudary
    y_right_top =325
    x_right_top =int(f_right(y_right_top))
    x_right_bottom = int(f_right(y_bottom)) # predict x coordiate for bottom ending points on the left bound
    cv2.line(img,(x_right_bottom,y_bottom),(x_right_top,y_right_top),color,thickness)
    
    

def hough_lines(img,rho,theta,threshold,min_line_len,max_line_gap):
    """apply Hough transformations to detect lines in images
    
       returns an image with Hough Lines drawn
    """
    
    # cv2.HoughLinesP returns two endingpoints(x,y) of lines.
    lines = cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)
    draw_lines(line_img,lines) 
    return line_img

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    
    return cv2.addWeighted(initial_img, α, img, β, γ)

vertices = np.array([[(100,540),(900,540),(475,300),(490,300)]]) # left bottom, right bottom and apex of triangle area
    
""" 
    main part to create the pipeline
"""    
input_directory = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_images/"
output_directory = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_images_output/"

canny_low = 50
canny_high = 150
hough_rho = 1 # rho step
hough_theta = np.pi/180 # theta step in radians
hough_threshold = 40
min_line_len = 10
max_line_gap = 30


# ================================================
#   Process All Images in Input Directory
# ================================================

for filename in os.listdir(input_directory):
    fig = plt.figure()
    image = input_image(input_directory+filename)
    plt.subplot(121)
    plt.imshow(image)
    image_process = grayscale(image) # transform to grey scale
    image_process = canny(image_process,canny_low,canny_high) # apply canny edge detector
    image_process = region_of_interest(image_process,vertices) # keep only area of interestes
    image_process = hough_lines(image_process,hough_rho,hough_theta,hough_threshold,min_line_len,max_line_gap) # apply hough transformation
    image_process = weighted_img(image_process,image) # combine line image and the original image
    plt.subplot(122)
    plt.imshow(image_process)
    plt.show()
    cv2.imwrite(output_directory+filename,cv2.cvtColor(image_process,cv2.COLOR_RGB2BGR))
    
# ================================================
#             Drawing lanes over video   
# ================================================
# Import everything needed to edit/save/watch video clips
from moviepy.editor import *
from IPython.display import HTML

def process_image(image):
    """ input is each frame/image in a clip """
    
    image_process = grayscale(image) # transform to grey scale
    image_process = canny(image_process,canny_low,canny_high) # apply canny edge detector
    image_process = region_of_interest(image_process,vertices) # keep only area of interestes
    image_process = hough_lines(image_process,hough_rho,hough_theta,hough_threshold,min_line_len,max_line_gap) # apply hough transformation
    image_process = weighted_img(image_process,image) # combine line image and the original image

    return image_process

def create_video(raw_video_path,output_path):
    raw_video = VideoFileClip(raw_video_path,audio=False)
    processed_clip = raw_video.fl_image(process_image)
    txt = TextClip("Produced by Wenbo Ma for Lane Detection - X coordinate-based weighted regression", font='Amiri-regular',
	               color='white',fontsize=20)
    txt_col= txt.on_color(size=(processed_clip.w + txt.w,txt.h-5),
                  color=(0,0,0), pos=(6,'center'), col_opacity=0.6)
    w,h = processed_clip.size
    txt_mov = txt_col.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)),40))
    composite_clip = CompositeVideoClip([processed_clip, txt_mov])
    composite_clip.subclip(0,processed_clip.duration).write_videofile(output_path,audio=False)
    raw_video.reader.close() # 
    del raw_video.reader #
    



# ======================================
#           process videos
# ======================================    

    
""" white lane video """
whitelane_video = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos/solidWhiteRight.mp4"
whitelane_output = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos_output/solidWhiteRight.mp4"
create_video(whitelane_video,whitelane_output)

""" yellow lane video """
yellowlane_output = 'E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos_output/solidYellowLeft.mp4'
yellowlane_video = 'E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos/solidYellowLeft.mp4'
create_video(yellowlane_video,yellowlane_output)

# =============================================================================
# """ """
# challenge_output = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos_output/challenge.mp4"
# challenge_video = "E:/Project/Udacity - Computer Vision/CarND-LaneLines-P1/test_videos/challenge.mp4"
# create_video(challenge_video,challenge_output)
# =============================================================================
