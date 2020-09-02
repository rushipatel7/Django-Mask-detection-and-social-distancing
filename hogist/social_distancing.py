import time
import cv2
import imutils
import numpy as np
from scipy.spatial import distance as dist
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(BASE_DIR + '/hogist/Models/yolov3-Social Distancing/coco.names', "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cfg_file = BASE_DIR + '/hogist/Models/yolov3-Social Distancing/yolov3-tiny.cfg'
weight_file = BASE_DIR + '/hogist/Models/yolov3-Social Distancing/yolov3-tiny.weights'
net = cv2.dnn.readNet(cfg_file, weight_file)

# if gpu is available
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 256)


class VideoCamera(object):
    def __init__(self):

        self.video = cv2.VideoCapture(BASE_DIR + "/hogist/sample videos/social-distancing.mp4")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        (grabbed, frame) = self.video.read()
        if not grabbed:
            exit()

        frame = imutils.resize(frame, width=700)
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

        end = time.time()
        bbox = []
        centroid = []
        confidence = []
        combi = []
        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %s" % (class_names, round(float(score[0]), 2))
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            confidence.append(float(score[0]))
            bbox.append([x, y, int(width), int(height)])
            centroid.append((centerX, centerY))

            combi.append([score[0], (x, y, int(width), int(height)), (centerX, centerY)])

        end_drawing = time.time()

        idxs = cv2.dnn.NMSBoxes(bbox, confidence, 0.3, 0.3)
        result = []
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (bbox[i][0], bbox[i][1])
                (w, h) = (bbox[i][2], bbox[i][3])

                # update our results list to consist of the person
                # prediction probability, bounding box coordinates,
                # and the centroid
                r = (confidence[i], (x, y, x + w, y + h), centroid[i])
                result.append(r)
        violate = set()
        if len(result) >= 2:
            centroids = np.array([r[2] for r in result])
            # print("\nIF MA GAYU ...", centroids)

            D = dist.cdist(centroids, centroids, metric="euclidean")
            # print("\nDDDDDD", D)

            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    MIN_DISTANCE = 100
                    if D[i, j] < MIN_DISTANCE:
                        violate.add(i)
                        violate.add(j)

        for (i, (prob, bbox, centroid)) in enumerate(result):
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)

            if i in violate:
                color = (0, 0, 255)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 1)

        text = "Social Distancing Violations: {}".format(len(violate))
        cv2.putText(frame, text, (10, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

        fps_label = "FPS: %.2f " % (
                1 / (end - start))

        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def index(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")