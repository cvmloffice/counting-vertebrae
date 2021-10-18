"""GUI to display yolo results in two axes

"""

#import ipdb
import sys
from pathlib import Path 
import os
import argparse

from collections import defaultdict
from io import StringIO

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import  Button, RadioButtons

parser = argparse.ArgumentParser(
    description="Run GUI to display YOLO results"
)
parser.add_argument('--image-list-path', required=True,
                    help="File containing path to images to open"
)
parser.add_argument('--bb-path-1', required=True,
                    help="File containing path to 1st set of bounding boxes"
)
parser.add_argument('--bb-path-2',
                    help="File containing path to 2nd set of bounding boxes"
)
parser.add_argument('-s', '--start-index', default=0,
                    type=int, help="Index to start at (0 based)"
)

args = parser.parse_args()

image_list = Path(args.image_list_path).read_text().split("\n")
bb1_list = Path(args.bb_path_1).read_text().split("\n")
if args.bb_path_2 is not None:
    bb2_list = Path(args.bb_path_2).read_text().split("\n")
else:
    bb2_list = []
n_images = len(image_list)

print(image_list)
print(n_images)

def onselect(eclick, erelease):
  'eclick and erelease are matplotlib events at press and release'
  print(' used button   : ', eclick.button)

class Index(object):
    ind = args.start_index
    ax = plt.gca()
    ax1 = None
    aximage1 = None
    ax2 = None
    aximage2 = None
    #n_images = len(mag_recs)
    n_images_minus_1 = n_images - 1
    str_n_images = str(n_images)

    def next(self, event):
        self.ind += 1
        ax.set_title('Iteration ' + str(self.ind))
        plt.show()

    def prev(self, event):
        self.ind -= 1
        ax.set_title('Iteration ' + str(self.ind))
        plt.show()

    def showNextImage(self, event):
        if self.ind < self.n_images_minus_1:
            self.ind += 1 
        self.show_image()

    def showPrevImage(self, event):
        if self.ind > 0:
            self.ind -= 1
        self.show_image()

    def process_click(self, event, name):
        #button = buttons[name]
        self.ind += 1
        ax.set_title('button clicked ' + str(self.ind))
        print(event)
        plt.show()

    def show_image(self):
        print(self.ind)
        im_path = image_list[self.ind]
        im = plt.imread(im_path)
        (ax1, aximage1) = self._show_image(self.ax1, self.aximage1, im, 1)
        (ax2, aximage2) = self._show_image(self.ax2, self.aximage2, im, 2)
        #if self.ax1 is None:
        #   self.ax1 = plt.subplot(121)
        #if self.aximage1 is None:
        #    self.aximage1 = self.ax1.imshow(im)
        #else:
        #    self.aximage1.set_data(im)
        #    # set extents as (xmin,xmax,ymax,ymin) so y axis origin at topleft
        #    self.aximage1.set_extent((0,im.shape[1],im.shape[0],0))
            
        self.set_title()
        self.im_width = im.shape[1]
        self.im_height = im.shape[0]
        
        # Set the class (radio button) if it already exists in list
        if len(image_list[self.ind]) > 1:
            im_class = image_list[self.ind][1]
            print( "Image is of class " + str(im_class))
        else:
            print("Image not yet classified")
        #try:

        #ipdb.set_trace()
        #self.draw_rect()
        plt.draw()
    
    def set_title(self):
        title = "X-ray image classification - manual"
        self.ax.set_title(title, fontsize=8)

    def _show_image(self, ax, aximage, im, ax_index):
        if ax is None:
           ax = plt.subplot(1,2,ax_index)
        if aximage is None:
            aximage = ax.imshow(im)
        else:
            aximage.set_data(im)
            # set extents as (xmin,xmax,ymax,ymin) so y axis origin at topleft
            aximage.set_extent((0,im.shape[1],im.shape[0],0))
        return (ax, aximage)

def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.ES.active:
        print(' EllipseSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.ES.active:
        print(' EllipseSelector activated.')
        toggle_selector.ES.set_active(True)


fig = plt.figure
global ax
ax = plt.subplot(111)

callback = Index()
callback.show_image()

left = 0.9
bottom = 0.05
width = 0.1
height = 0.075
offset = 0.01
buttons = {
    'showNextImage': {'index': 3, 'callback': callback.showNextImage}, 
    'showPrevImage': {'index': 2, 'callback': callback.showPrevImage},
#    'saveToFile': {'index': 1, 'callback': callback.saveToFile}
}

for key in buttons.keys():
    button = buttons[key]
    bottom2 = bottom + button['index'] * (height + offset)
    button['axhandle'] = plt.axes([left, bottom2, width, height])
    button['handle'] = Button(button['axhandle'], key)
    button['handle'].on_clicked(button['callback'])
    
# Radiobuttons
left = 0.05
bottom = 0.7
width = 0.15
height = 0.15
offset = 0.01
radio_buttons = {
    'showNextImage': {'index': 3, 'callback': callback.showNextImage}, 
    'showPrevImage': {'index': 2, 'callback': callback.showPrevImage},
#    'saveToFile': {'index': 1, 'callback': callback.saveToFile}
}

rax = plt.axes([left,bottom,width,height])
radio = RadioButtons(rax, ('whole mouse','skull','right paw','left paw','other'))

plt.show()
