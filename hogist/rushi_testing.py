import time
import cv2
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import os

from requests import Response

from hogist import VideoGet
from hogist.models import userIpdetails

f = userIpdetails.objects.latest('id')
path = f.ip_address
print("BHJWCBCW", f.ip_address)

# open any valid video stream(for e.g `test.mp4` file)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(BASE_DIR + '/hogist/Models/yolov3-Mask Detection/coco.names', "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cfg_file = BASE_DIR + '/hogist/Models/yolov3-Mask Detection/yolov3-tiny-obj.cfg'
weight_file = BASE_DIR + '/hogist/Models/yolov3-Mask Detection/yolov3-tiny-obj_last (12).weights'
net = cv2.dnn.readNet(cfg_file, weight_file)

# if gpu is available
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 256)

# path = 'http://192.168.0.100:8080/video'

with_mask = 0
without_mask = 0


class VideoCamera(object):
    def __init__(self):
        # # print("SESSS", ip)
        # # self.video = cv2.VideoCapture('http://192.168.0.100:8080/video')
        # self.video = cv2.VideoCapture(path)
        self.video = VideoGet(path).start()
        # self.video = cv2.VideoCapture(BASE_DIR + "/hogist/sample videos/m1.mp4")

        # Define Netgear Server with default parameters

    def __del__(self):
        self.video.release()

    def get_frame(self):
        f = userIpdetails.objects.latest('id')
        (grabbed, frame) = self.video.read()
        if not grabbed:
            exit()

        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        start_drawing = time.time()
        global with_mask, without_mask
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %s" % (class_names[classid[0]], round(float(score[0]), 2))
            label1 = class_names[classid[0]]

            if label1 == 'with_mask':

                with_mask += 1
            else:

                without_mask += 1

            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        end_drawing = time.time()

        with_mask_number = int(round(with_mask // (1 / (end - start)), 1))
        without_mask_number = int(round(without_mask // (1 / (end - start)), 1))

        show_with_mask = "With Mask %.1f" % with_mask_number
        show_without_mask = "Without Mask %.1f" % without_mask_number
        print("Show", show_with_mask)
        # request.session['mask'] = with_mask_number
        # f = userIpdetails.objects.latest('id')

        if f.id:
            f.with_mask_count = with_mask_number
            f.without_mask_count = without_mask_number
            f.save()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (
            1 / (end - start), (end_drawing - start_drawing) * 1000)
        # cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, show_with_mask, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, show_without_mask, (325, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # cv2.imshow("detections", frame)
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
        return Response(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
