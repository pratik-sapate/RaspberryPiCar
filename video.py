import numpy as np
import os
import cv2
import sys
import tensorflow as tf


sys.path.append("..")
if tf.__version__>'1.4.0':
    raise ImportError("Please upgrade your tensorflow installation to v1.4.* or latter")

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils

MODEL_NAME = "ssd_mobilenet_v1_coco_2018_01_28"
MODEL_FILE = MODEL_NAME + ".tar.gz"
DOWNLOAD_BASE = "http://download.tensorflow.org/models/object_detection/"

PATH_TO_TEST_IAMGE_DIR = 'models/research/object_detection/test_images/Pratik_photos'

PATH_TO_CKPT = MODEL_NAME+'/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('models/research/object_detection/data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES)
categories_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=detection_graph)

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value

TEST_IMAGE_PATH = os.path.join(PATH_TO_TEST_IAMGE_DIR, 'test1.jpg')
TEST_VIDEO_PATH = os.path.join(PATH_TO_TEST_IAMGE_DIR, 'video_20170219_105023.mp4')
video = cv2.VideoCapture(0)

while video.isOpened():
    ret, frame = video.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_expanded = np.expand_dims(image_rgb, axis=0)
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Draw the results of the detection (aka 'visulaize the results')

    visualization_utils.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        categories_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)

    # All the results have been drawn on image. Now display the image.
    cv2.namedWindow('Object detector', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Object detector', 640, 420)
    cv2.imshow('Object detector', frame)

    # Press any key to close the image
    cv2.waitKey(0)

# Clean up
video.release()
cv2.destroyAllWindows()
