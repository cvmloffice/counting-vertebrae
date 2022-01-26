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

#print(image_list)
#print(n_images)

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

    def show_image(self):
        #print(self.ind)
        im_path = image_list[self.ind]
        im = plt.imread(im_path)
        (self.ax1, self.aximage1) = self._show_image(self.ax1, self.aximage1, im, 1)
        (self.ax2, self.aximage2) = self._show_image(self.ax2, self.aximage2, im, 2)
        
        self._set_title(self.ax1)
        #self._set_title(self.ax2)
        self.im_width = im.shape[1]
        self.im_height = im.shape[0]
        
        # Plot the bounding boxes
        self._show_bb( self.ax1, bb1_list[self.ind], "g")
        self._show_bb( self.ax2, bb2_list[self.ind], "r")

        #ipdb.set_trace()
        #self.draw_rect()
        plt.draw()
    
    def _set_title(self, ax):
        im_name = os.path.split(image_list[self.ind])[-1]
        title = f"Image {self.ind+1} of {n_images} - {im_name}"
        plt.suptitle(title, fontsize=8)

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

    def _show_bb(self, ax, bb_path, color='r'):
        _ , bb1 = self._read_bounding_box(bb_path)
        ax.lines.clear()
        for bb in self._scale_bb(bb1, self.im_width, self.im_height):
            ax.plot([bb[0], bb[0], bb[2], bb[2], bb[0]],
                    [bb[1], bb[3], bb[3], bb[1], bb[1]], color)

    #TODO: Move this function to a general utilities package
    def _read_bounding_box(self, bb_path):
        """Read bounding box for an image"""

        with open(bb_path, "rt") as fid:
            bb = [ [float(l2) for l2 in l.strip("\n").split(" ")] for l in fid.readlines()]
    
        bb = np.array(bb)
    
        # Return labels and bbs separately
        return bb[:,0], bb[:,1:]
    
    #TODO: Move this function to a general utilities package
    def _scale_bb(self, bbs, width, height):
        scale = np.array((width, height, width, height), dtype=float)
        bbs_scaled = []
        for bb in bbs:
            x_start = bb[0] - bb[2]/2
            y_start = bb[1] - bb[3]/2
            x_end = x_start + bb[2]
            y_end = y_start + bb[3]
            bbs_scaled.append(np.array((x_start, y_start, x_end, y_end) * scale, dtype=int))
        return bbs_scaled

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
    
plt.show()
