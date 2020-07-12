import numpy as np
import os
import cv2
import sys
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils

class objectDetect:
    def __init__(self):
        self.MODEL_NAME = "ssd_mobilenet_v1_coco_2018_01_28"
        self.MODEL_FILE = self.MODEL_NAME + ".tar.gz"
        # self.DOWNLOAD_BASE = "http://download.tensorflow.org/models/object_detection/"

        self.PATH_TO_TEST_IAMGE_DIR = 'models/research/object_detection/test_images/Pratik_photos'

        self.PATH_TO_CKPT = self.MODEL_NAME + '/frozen_inference_graph.pb'
        self.PATH_TO_LABELS = os.path.join('models/research/object_detection/data', 'mscoco_label_map.pbtxt')
        self.NUM_CLASSES = 90

        self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.NUM_CLASSES)
        self.categories_index = label_map_util.create_category_index(self.categories)
        # Load the Tensorflow model into memory.
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.sess = tf.Session(graph=self.detection_graph)

        # Input tensor is the image
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def detect_object_from_image(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes,
             self.detection_scores,
             self.detection_classes,
             self.num_detections],
            feed_dict={self.image_tensor: image_expanded})

        # Draw the results of the detection (aka 'visulaize the results')

        visualization_utils.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.categories_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

        # All the results have been drawn on image. Now display the image.
        # cv2.namedWindow('Object detector', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Object detector', 640, 420)
        # cv2.imshow('Object detector', frame)

        # Press any key to close the image
        # cv2.waitKey(0)
        return frame

if __name__=='__main__':
    obj = objectDetect()
    video = cv2.VideoCapture(0)
    while video.isOpened():
        ret, frame = video.read()
        frame = obj.detect_object_from_image(frame)
        cv2.namedWindow('Object detector', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object detector', 640, 420)
        cv2.imshow('Object detector', frame)

        # Press any key to close the image
        cv2.waitKey(0)
    video.release()
    cv2.destroyAllWindows()