import json
import os
import cv2 as cv
import numpy as np
import socketio

net = cv.dnn.readNet("yolo.weights", "yolo.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

rate = 2

cap1 = cv.VideoCapture(0)
cap2 = cv.VideoCapture(2)
cap1.set(3, 640)
cap1.set(4, 480)
cap2.set(3, 640)
cap2.set(4, 480)

sock = socketio.Client()
sock.connect('http://192.168.43.187:33333')
check = 0
while True:

    ret, temp1 = cap1.read()
    ret, temp2 = cap2.read()

    frame = cv.hconcat([temp1, temp2])
    # frame = temp1

    # frame = cv.resize(frame, None, fx=rate, fy=rate)

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id == 0:
                confidence = scores[class_id]  # 62번 tv 모니터
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

                    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if len(boxes) == 2:
            x1, y1, w1, h1 = boxes[0]
            x2, y2, w2, h2 = boxes[1]
            label1 = str(classes[class_ids[0]])
            label2 = str(classes[class_ids[1]])
            color1 = colors[0]
            color2 = colors[1]
            cv.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), color1, 2)
            cv.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), color2, 2)
            # cv.putText(frame, label1, (x1, y1 + 30), font, 3, color1, 3)
            # cv.putText(frame, label2, (x2, y2 + 30), font, 3, color2, 3)
            cv.putText(frame, str(x1 + w1 / 2 - 320), (x1, y1 + 30), font, 3, color1, 3)
            cv.putText(frame, str(x2 + w2 / 2 - 320 - 640), (x2, y2 + 30), font, 3, color2, 3)
            t1 = (x1 + w1 / 2 - 320)
            t2 = (x2 + w2 / 2 - 320) - 640
            t3 = np.abs(t1 - t2)
            distance = (-6.5 * t3 + 558.5) / 100
            #os.system('say 물체인식')
            if check == 0:
                sock.emit("puto", json.dumps([{'dist': distance, 'px': t1, 'type': label1}]))
                sock.emit("putttt", 5)
                check = 1
            ''' 
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(frame, label, (x, y + 30), font, 3, color, 3)
            '''

    #engine.runAndWait()
    cv.imshow('ImageWindow', frame)
    cv.waitKey(1)
