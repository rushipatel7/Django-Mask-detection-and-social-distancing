import datetime
# opencvheadless
import threading
import psycopg2
from django.contrib import auth, messages
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import extendUserDetails
from hogist.models import userIpdetails
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import time
import cv2
import imutils
import numpy as np
from scipy.spatial import distance as dist
import os
from hogist import testing_mask as md


# Create your views here.

@login_required(login_url='login')
def index(request):
    withmask_count = []
    withoutmask_count = []

    conn = psycopg2.connect(
        host="ls-0438f08a704227d445cfa8ff64e4f7df8e84bb1e.cu81vx4tdqjc.ap-south-1.rds.amazonaws.com",
        database="dbaimaster", port=5432, user='dbmasteruser', password='a+5[8ql+{frL>S!gO).QFrxjxor:;B>u')
    curr = conn.cursor()

    query = """ SELECT * FROM user_ipdetails ORDER BY id desc """
    curr.execute(query)
    rows = curr.fetchall()[0]
    mask = rows[3]
    no_mask = rows[4]

    social_dis = rows[6]
    withmask_count.append(mask)
    withoutmask_count.append(no_mask)

    query1 = """ SELECT * FROM user_ipdetails where email = '{0}' """
    e = query1.format(request.user.email)
    curr.execute(e)
    rows1 = curr.fetchall()
    alltime_mask_mon, alltime_mask_tue, alltime_mask_wed, alltime_mask_thu, alltime_mask_fri, alltime_mask_sat, alltime_mask_sun = (
        [] for i in range(7))
    alltime_no_mask_mon, alltime_no_mask_tue, alltime_no_mask_wed, alltime_no_mask_thu, alltime_no_mask_fri, alltime_no_mask_sat, alltime_no_mask_sun = (
        [] for i in range(7))
    social_dis_mon, social_dis_tue, social_dis_wed, social_dis_thu, social_dis_fri, social_dis_sat, social_dis_sun = (
        [] for i in range(7)
    )
    time_mon, time_tue, time_wed, time_thu, time_fri, time_sat, time_sun = ([] for i in range(7))
    today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    thres_day = today - datetime.timedelta(days=today.weekday())  # thresold day
    for i in rows1:
        if i != 'None':
            w = i[3]
            x = i[4]
            t = i[5]
            s = i[6]
            # alltime_no_mask.append(x)
            if t > thres_day:
                if t.strftime('%a') == 'Mon':
                    alltime_mask_mon.append(w)
                    alltime_no_mask_mon.append(x)
                    time_mon.append(t.strftime('%a'))
                    social_dis_mon.append(s)
                elif t.strftime('%a') == 'Tue':
                    alltime_mask_tue.append(w)
                    alltime_no_mask_tue.append(x)
                    time_tue.append(t.strftime('%a'))
                    social_dis_tue.append(s)
                elif t.strftime('%a') == 'Wed':
                    alltime_mask_wed.append(w)
                    alltime_no_mask_wed.append(x)
                    time_wed.append(t.strftime('%a'))
                    social_dis_wed.append(s)
                elif t.strftime('%a') == 'Thu':
                    alltime_mask_thu.append(w)
                    alltime_no_mask_thu.append(x)
                    time_thu.append(t.strftime('%a'))
                    social_dis_thu.append(s)
                elif t.strftime('%a') == 'Fri':
                    alltime_mask_fri.append(w)
                    alltime_no_mask_fri.append(x)
                    time_fri.append(t.strftime('%a'))
                    social_dis_fri.append(s)
                elif t.strftime('%a') == 'Sat':
                    alltime_mask_sat.append(w)
                    alltime_no_mask_sat.append(x)
                    time_sat.append(t.strftime('%a'))
                    social_dis_sat.append(s)
                elif t.strftime('%a') == 'Sun':
                    alltime_mask_sun.append(w)
                    alltime_no_mask_sun.append(x)
                    time_sun.append(t.strftime('%a'))
                    social_dis_sun.append(s)
    t = 0
    if time_mon == [] or time_tue == [] or time_wed == [] or time_thu == [] or time_fri == [] or time_sat == [] or time_sun == []:
        time_mon.append(t)
    res_mask_mon = [i for i in alltime_mask_mon if i]
    res_mask_tue = [i for i in alltime_mask_tue if i]
    res_mask_wed = [i for i in alltime_mask_wed if i]
    res_mask_thu = [i for i in alltime_mask_thu if i]
    res_mask_fri = [i for i in alltime_mask_fri if i]
    res_mask_sat = [i for i in alltime_mask_sat if i]
    res_mask_sun = [i for i in alltime_mask_sun if i]

    res_nomask_mon = [i for i in alltime_no_mask_mon if i]
    res_nomask_tue = [i for i in alltime_no_mask_tue if i]
    res_nomask_wed = [i for i in alltime_no_mask_wed if i]
    res_nomask_thu = [i for i in alltime_no_mask_thu if i]
    res_nomask_fri = [i for i in alltime_no_mask_fri if i]
    res_nomask_sat = [i for i in alltime_no_mask_sat if i]
    res_nomask_sun = [i for i in alltime_no_mask_sun if i]

    res_social_dis_mon = [i for i in social_dis_mon if i]
    res_social_dis_tue = [i for i in social_dis_tue if i]
    res_social_dis_wed = [i for i in social_dis_wed if i]
    res_social_dis_thu = [i for i in social_dis_thu if i]
    res_social_dis_fri = [i for i in social_dis_fri if i]
    res_social_dis_sat = [i for i in social_dis_sat if i]
    res_social_dis_sun = [i for i in social_dis_sun if i]

    content = {
        'mask_count': mask,
        'no_mask_count': no_mask,

        'mask_mon': sum(res_mask_mon),
        'mask_tue': sum(res_mask_tue),
        'mask_wed': sum(res_mask_wed),
        'mask_thu': sum(res_mask_thu),
        'mask_fri': sum(res_mask_fri),
        'mask_sat': sum(res_mask_sat),
        'mask_sun': sum(res_mask_sun),

        'nomask_mon': sum(res_nomask_mon),
        'nomask_tue': sum(res_nomask_tue),
        'nomask_wed': sum(res_nomask_wed),
        'nomask_thu': sum(res_nomask_thu),
        'nomask_fri': sum(res_nomask_fri),
        'nomask_sat': sum(res_nomask_sat),
        'nomask_sat': sum(res_nomask_sun),

        'social_mon': sum(res_social_dis_mon),
        'social_tue': sum(res_social_dis_tue),
        'social_wed': sum(res_social_dis_wed),
        'social_thu': sum(res_social_dis_thu),
        'social_fri': sum(res_social_dis_fri),
        'social_sat': sum(res_social_dis_sat),
        'social_sun': sum(res_social_dis_sun),
    }

    return render(request, 'index.html', content)


def landing(request):
    return render(request, 'landing.html')


def logout(request):
    auth.logout(request)
    return render(request, 'landing.html')


@login_required(login_url='login')
def mask_ip_details(request):
    if request.method == 'POST':
        get_ip = request.POST.get('addIpAddress')
        print(get_ip)

        current_email = request.user.email
        save_ip = userIpdetails()
        save_ip.ip_address = get_ip
        save_ip.email = current_email
        save_ip.time = datetime.datetime.now()
        save_ip.save()

        if get_ip != '':
            request.session['ip_value'] = get_ip
            print("Session", request.session.get('ip_value'))
            # return redirect('mask')
        return render(request, 'mask_detection.html', {'ip': get_ip})
        # return render(request, 'index.html')

    return render(request, 'mask_detection.html')


@login_required(login_url='login')
def social_dis_ip_details(request):
    if request.method == 'POST':
        social_ip = request.POST.get('addIpAddressSocial')
        # social_port = request.POST.get('addPortNumberSocial')

        # print(social_ip, social_port)

        # social_cctv = 'https://' + social_ip + ':' + social_port + '/video'

        current_email = request.user.email
        save_ip = userIpdetails()
        save_ip.ip_address = social_ip
        save_ip.email = current_email
        save_ip.time = datetime.datetime.now()
        save_ip.save()

        if social_ip != '':
            request.session['social_ip'] = social_ip
            print("IP ", request.session.get('social_ip'))
            return render(request, 'social_distancing.html', {'social_ip': social_ip})
    return render(request, 'social_distancing.html')


# def streaming(request):
#     ip = request.session.get('ip_value')
#     vs = StreamingHttpResponse(md.gen(md.VideoCamera(ip)), status=200,
#                                content_type="multipart/x-mixed-replace;boundary=frame")
#     vs['Cache-Control'] = 'no-cache'
#     return vs

def streaming(request):
    ip = request.session.get('ip_value')
    vs = StreamingHttpResponse(md.gen(md.VideoCamera()), status=200,
                               content_type="multipart/x-mixed-replace;boundary=frame")
    vs['Cache-Control'] = 'no-cache'
    return vs



def stream_mask(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    CONFIDENCE_THRESHOLD = 0.5
    NMS_THRESHOLD = 0.4
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

    class_names = []
    with open(BASE_DIR + '/hogist/Models/yolov3-Mask Detection/coco.names', "r") as f:
        # with open(BASE_DIR + '/hogist/Models/yolov3_mask(v3)/coco.names', "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    # cfg_file = BASE_DIR + '/hogist/Models/yolov3_mask(v3)/yolov3.cfg'
    # weight_file = BASE_DIR + '/hogist/Models/yolov3_mask(v3)/yolov3_mask_last.weights'
    # net = cv2.dnn.readNet(cfg_file, weight_file)

    cfg_file = BASE_DIR + '/hogist/Models/yolov3-Mask Detection/yolov3-tiny-obj.cfg'
    weight_file = BASE_DIR + '/hogist/Models/yolov3-Mask Detection/yolov3-tiny-obj_last (12).weights'
    net = cv2.dnn.readNet(cfg_file, weight_file)

    get_ip = request.session.get('ip_value')
    print("IP VALUE ", get_ip)
    vc = cv2.VideoCapture(get_ip)
    # vc = cv2.VideoCapture(BASE_DIR + "/hogist/sample videos/m3.mp4")

    # if gpu is available
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 256)
    global with_mask, with_mask_number
    global without_mask
    with_mask = 0
    without_mask = 0
    while True:
        (grabbed, frame) = vc.read()
        # threading.Thread().start()
        if not grabbed:
            # exit()
            break
        s = time.time()
        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s" % (class_names[classid[0]])
            # label = "%s : %s" % (class_names[classid[0]], round(float(score[0]), 2))
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
        global show_with_mask, show_without_mask
        show_with_mask = "With Mask %.1f" % with_mask_number
        show_without_mask = "Without Mask %.1f" % without_mask_number
        request.session['mask'] = with_mask_number
        f = userIpdetails.objects.latest('id')

        if f.id:
            f.with_mask_count = with_mask_number
            f.without_mask_count = without_mask_number
            f.save()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (
            1 / (end - start), (end_drawing - start_drawing) * 1000)
        # cv2.putText(frame, fps_label, (25, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, show_with_mask, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, show_without_mask, (325, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        img_name = request.user.email
        img_name = request.session.get('ip_value')
        img_name = img_name.replace('.', '')
        img_name = img_name.replace('/', '')
        img_name = img_name.replace(':', '')

        # img_name = 'rruni'
        # print("IMAG",img_name)
        cv2.imwrite('./stream_image/mask/' + img_name + 'mask.jpg', frame)

        try:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open(
                './stream_image/mask/' + img_name + 'mask.jpg', 'rb').read() + b'\r\n')
        except:
            pass


def stream_social_dis(request):
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

    get_ip = request.session.get('social_ip')
    print("IP VALUE ", get_ip)
    vc = cv2.VideoCapture(get_ip)
    # vc = cv2.VideoCapture(BASE_DIR + "/hogist/sample videos/social-distancing.mp4")

    # if gpu is available
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 256)
    social_dis_count = 0
    while True:
        (grabbed, frame) = vc.read()
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

            D = dist.cdist(centroids, centroids, metric="euclidean")

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
                social_dis_count += 1
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 1)

        text = "Social Distancing Violations: {}".format(len(violate))

        show_count = round(social_dis_count // (1 / (end - start)), 1)
        show_dis_count = "Don't Follow Rule  %.1f" % show_count

        f = userIpdetails.objects.latest('id')
        if f.id:
            f.social_dis = show_count
            f.save()

        request.session['social_count'] = show_count
        cv2.putText(frame, show_dis_count, (300, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)
        cv2.putText(frame, text, (10, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

        fps_label = "FPS: %.2f " % (
                1 / (end - start))

        # cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        img_name = request.session.get('social_ip')
        img_name = img_name.replace('.', '')
        img_name = img_name.replace('/', '')
        img_name = img_name.replace(':', '')
        cv2.imwrite('./stream_image/social_dis/' + img_name + "social_dis.jpg", frame)
        try:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open(
                './stream_image/social_dis/' + img_name + 'social_dis.jpg', 'rb').read() + b'\r\n')
        except:
            pass


@login_required(login_url='login')
def show_mask_stream(request):
    return StreamingHttpResponse(stream_mask(request), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def show_social_dis_stream(request):
    return StreamingHttpResponse(stream_social_dis(request), content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url='login')
def social_distancing(request):
    return render(request, 'social_distancing.html')


@login_required(login_url='admin-login')
def admin_index(request):
    return render(request, 'admin/admin-index.html')


@login_required(login_url='login')
def user_setting(request):
    current_user_email = request.user.email
    current_user_firstname = request.user.first_name
    current_user_lastname = request.user.last_name
    current_user_username = request.user.username
    current_user_last_login = request.user.last_login
    current_user_date_join = request.user.date_joined

    user_info = extendUserDetails.objects.get(email=current_user_email)
    print("USXRCX", user_info.company_name)
    current_user_companyname = user_info.company_name
    current_user_mobilenumber = user_info.mobile_number

    data = {
        'email': current_user_email,
        'first_name': current_user_firstname,
        'last_name': current_user_lastname,
        'username': current_user_username,
        'last_login': current_user_last_login,
        'created_at': current_user_date_join,
        'company_name': current_user_companyname,
        'mobile_number': current_user_mobilenumber
    }
    return render(request, 'User/user_setting.html', data)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })


