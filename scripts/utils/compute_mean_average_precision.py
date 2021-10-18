"""Given two sets of bounding boxes, compute mean average precision as intersection/union

"""
# Usage: compute_mean_average_prediction.py path_to_images.txt_file
# Accept .txt file like YOLO
#   .txt path has full path to images
#   path to ground truth is path_to_images/../labels
#   path to predictions is path_to_images/../predicted_labels
#

# Assume python > 3.6

import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

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

def _scale_bb(bbs, width, height):
    scale = np.array((width, height, width, height), dtype=float)
    bbs_scaled = []
    for bb in bbs:
        x_start = bb[0] - bb[2]/2
        y_start = bb[1] - bb[3]/2
        x_end = x_start + bb[2]
        y_end = y_start + bb[3]
        bbs_scaled.append(np.array((x_start, y_start, x_end, y_end) * scale, dtype=int))
    return bbs_scaled


def _plot_rects(im, bb1, bb2, ax=None):
    """Plot rectangles of bounding boxes on image"""
    if ax is None:
        ax=plt.gca()
    ax.imshow(im)

    height, width = im.shape[0:2]
    for bb in _scale_bb(bb1, width, height):
        ax.plot([bb[0], bb[0], bb[2], bb[2], bb[0]],[bb[1],bb[3], bb[3], bb[1], bb[1]], 'r')
    for bb in _scale_bb(bb2, width, height):
        ax.plot([bb[0], bb[0], bb[2], bb[2], bb[0]],[bb[1],bb[3], bb[3], bb[1], bb[1]], 'b')
    return ax
        

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
    parser = argparse.ArgumentParser(
        description = "Compute mean average precision"
    )
    parser.add_argument("-i", dest="input_path", required=True,
        help="Path to file containing paths to images"
    )
    parser.add_argument("-g", dest="gt_path", default="../labels",
        help="Relative path to ground truth"
    )
    parser.add_argument("-p", dest="pred_path", default="../predictions",
        help="Relative path to ground truth"
    )
    parser.add_argument("-o", dest="output_path", default="./mean_average_precision.csv",
        help="Path to save output"
    )
    parser.add_argument("-m", "--montage", dest="montage", 
        default=False, action='store_true',
        help="Create montage of overlay of groundtruth and predictions"
    )
    parser.add_argument("--ncols", dest="ncols", type=int, default=3,
        help="Number of columns for montage"
    )
    parser.add_argument("--nrows", dest="nrows", type=int, default="6",
        help="Maximum number of rows per page"
    )
    parser.add_argument("--gt-colour", dest="gt_color", default="r",
        help="Color for ground truth rectangles"
    )
    parser.add_argument("--pred-colour", dest="pred_color", default="g",
        help="Color for predicted rectangles"
    )

    args = parser.parse_args()
    input_path = args.input_path
    gt_path = args.gt_path
    pred_path = args.pred_path
    
    # Get list of images
    with open(input_path, "rt") as fid:
        images_to_process = [i.strip() for i in fid.readlines()]
    
    n_images = len(images_to_process)
    print(f"N images = {n_images}")

    if args.montage:
        ncols = int(np.min((n_images, args.ncols)))
        #nrows = int(np.ceil(n_images/ncols))
        nrows = args.nrows
        fig, axs = plt.subplots(nrows, ncols, figsize=(7,9),
                                subplot_kw={'xticks': [], 'yticks': []})
        n_per_page = ncols * nrows
        # Take away 1 because of zero offset

    # Get mAP for each image
    mean_average_precision = ""
    for i, image_path in enumerate(images_to_process, start=0):
        # Open image and get width/height
        im = plt.imread(image_path)
        height, width = im.shape[0:2]

        # Read ground truth bounding boxes
        labels_gt, bb_gt = _read_bounding_box(image_path, gt_path)
        labels_pred, bb_pred = _read_bounding_box(image_path, pred_path)
        m_ap = _compute_mean_average_precision(width, height, bb_gt, bb_pred)
        mean_average_precision += f"{image_path},{m_ap}\n"

        # If necessary plot gt and prediction
        if args.montage:
            row = int(np.floor(i/ncols))
            col = i%ncols
            print(f"row={row}, col={col}")
            if nrows < 2:
                ax = axs[col]
            else:
                ax = axs[row][col]
            _plot_rects(im, bb_gt, bb_pred, ax)

            image_name = Path(image_path).name
            ax.set_title(f"{image_name} - {m_ap:.2f}")
            
    
    # Write out processed values
    output_path = args.output_path
    
    with open(output_path, "wt") as fid:
        fid.writelines(mean_average_precision)

    # Compute montage if required
    if args.montage:
        montage_path = os.path.splitext(output_path)[0] + ".png"
        plt.savefig(montage_path)
        
        
if __name__ == "__main__":
    main()
    
