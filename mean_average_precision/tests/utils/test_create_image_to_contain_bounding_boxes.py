"""Given bounding boxes, test image with minimum dims containing all returned

"""
# Usage: compute_mean_average_prediction.py path_to_images.txt_file
# Accept .txt file like YOLO
#   .txt path has full path to images
#   path to ground truth is path_to_images/../labels
#   path to predictions is path_to_images/../predicted_labels
#

# Assume python > 3.6

import os
import numpy as np
import matplotlib.pyplot as plt

def _read_bounding_box(image_path, bb_rel_path=None):
    """Read bounding box for an image"""

    # Image path is path to image
    # bb_rel_path is list containing relative path to bb from image dir
    
    if bb_rel_path is None:
        bb_rel_path = ""
    elif type(bb_rel_path) == list:
        bb_rel_path = os.path.sep.join(bb_rel_path)

    im_dir, fname = os.path.split(image_path)
    fname = os.path.splitext(fname)[0] + ".txt"
    bb_path = os.path.join(im_dir,bb_rel_path, fname)
    with open(bb_path, "rt") as fid:
        bb = [ [float(l2) for l2 in l.strip("\n").split(" ")] for l in fid.readlines()]

    bb = np.array(bb)

    # Return labels and bbs separately
    return bb[:,0], bb[:,1:]


def _compute_mean_average_precision(width, height, bb1, bb2):
    """Compute the mean average precision given bounding box and im size"""

    # Inputs: path to image, path to ground truth bbs, path to predicted bbs
    # Assume yolo format for bbs:
    #   label xc, yc, w, h
    #       xc,yc are relative to top-left of image and normalised by image w/h
    #       w,h are also normalised by image w/h

    
    im_gt = np.full((width, height), fill_value=False, dtype=bool)
    im_pred = np.full((width, height),fill_value=False,  dtype=bool)

    # For each bounding box scale to dimensions of real image
    scale = np.array((width, height, width, height), dtype=float)
    for bb in bb1:
        x_start = bb[0] - bb[2]/2
        y_start = bb[1] - bb[3]/2
        x_end = x_start + bb[2]
        y_end = y_start + bb[3]
        x_start, y_start, x_end, y_end = np.array((x_start, y_start, x_end, y_end) * scale, dtype=int)

        im_gt[x_start:x_end, y_start:y_end] = True
        #print(f"{x_start},{x_end},{y_start},{y_end}")
        #im_gt[0:10, 20:30] = True

    for bb in bb2:
        x_start = bb[0] - bb[2]/2
        y_start = bb[1] - bb[3]/2
        x_end = x_start + bb[2]
        y_end = y_start + bb[3]
        x_start, y_start, x_end, y_end = np.array((x_start, y_start, x_end, y_end) * scale, dtype=int)

        im_pred[x_start:x_end, y_start:y_end] = True

    return len(np.where(im_gt & im_pred)[0]) / len(np.where(im_gt | im_pred)[0])
    

def main():
    import sys
    input_path = sys.argv[1]
    
    # Get list of images
    with open(input_path, "rt") as fid:
        images_to_process = [i.strip() for i in fid.readlines()]
    
    # Get mAP for each image
    mean_average_precision = ""
    for image_path in images_to_process:
        # Open image and get width/height
        im = plt.imread(image_path)
        height, width = im.shape[0:2]

        # Read ground truth bounding boxes
        labels_gt, bb_gt = _read_bounding_box(image_path, ["..", "labels"])
        m_ap = _compute_mean_average_precision(width, height, bb_gt, bb_gt)
        mean_average_precision += f"{image_path},{m_ap}\n"
    
    # Write out processed values
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = "mean_average_precision.csv"
    
    with open(output_path, "wt") as fid:
        fid.writelines(mean_average_precision)


if __name__ == "__main__":
    main()
    
