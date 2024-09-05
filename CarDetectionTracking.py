import cv2 as cv
from ultralytics import YOLO
import imutils
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np


def processVideo():
    counter_cache = []
    detection_classes= []
    count = 0
    path = "resources/cars_in_dtu.mp4" \
           "" \
           "" \
           ""
    #read video
    vs = cv.VideoCapture(path)
    #load the model
    model = YOLO('yolov8n.pt')

    object_tracker = DeepSort(max_iou_distance=0.7,
                              max_age=5,
                              n_init=3,
                              nms_max_overlap=1.0,
                              max_cosine_distance=0.2,
                              nn_budget=None,
                              gating_only_position=False,
                              override_track_class=None,
                              embedder="mobilenet",
                              half=True,
                              bgr=True,
                              embedder_gpu=True,
                              embedder_model_name=None,
                              embedder_wts=None,
                              polygon=False,
                              today=None
                              )


    while True:
        (grabbed,img) = vs.read()
        frame = cv.resize(img, (0, 0), fx=0.6, fy=0.4)
        if not grabbed:
            break

        results = model.predict(frame,stream=False,classes = [2])
        print(results[0].names)
        detection_classes = results[0].names
        frame = draw_line(frame)
        for result in results:
            for data in result.boxes.data.tolist():
                #print(data)
                id = data[5]
                drawBox(data, frame,detection_classes[id])

                print("detected class:--",detection_classes[id])


            details = get_details(result,frame)
            tracks = object_tracker.update_tracks(details, frame=frame)



        for track in tracks:
            if not track.is_confirmed():
                break
            track_id = track.track_id
            bbox = track.to_ltrb()

            cv.putText(frame, "ID: " + str(track_id), (int(bbox[0]), int(bbox[1])), cv.FONT_HERSHEY_SIMPLEX, 1,
                       (0, 255, 0), 6)
            cv.putText(frame, "Vehicle Count: " + str(count), (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (200, 150, 255),
                       4)

            if bbox[1] >  3*int(frame.shape[0]/4) and track_id not in counter_cache:
                counter_cache.append(track_id)
                count = count + 1




        #show frames
        cv.imshow('image', frame)
        if cv.waitKey(1)& 0xFF == ord('q'):
            break


def drawBox(data,image,name):
    x1, y1, x2, y2, conf, id = data
    p1 = (int(x1), int(y1))
    p2 = (int(x2), int(y2))
    cv.rectangle(image, p1, p2, (255, 255, 255), 2)
    cv.putText(image, name, p1, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image

def get_details(result,image):
    classes = result.boxes.cls.numpy()
    conf = result.boxes.conf.numpy()
    xywh = result.boxes.xywh.numpy()

    detections = []
    for i,item in enumerate(xywh):
        sample = (item,conf[i] ,classes[i])
        detections.append(sample)

    return detections

def draw_line(image):
    depth = 3* int(image.shape[0]/4)
    p1 = (300,depth)
    p2 = (image.shape[1]-200,depth)
    print(p1,p2)
    image = cv.line(image, p1, p2, (100, 255, 0), thickness=6)

    return image


processVideo()






