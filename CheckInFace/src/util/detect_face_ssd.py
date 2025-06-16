import numpy as np
import cv2

def detect_face_ssd(orig_frame, network, conf_min=0.7, show_conf=True):
    frame = orig_frame.copy()  # to keep the original frame intact (just if we want to save the full image
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
    network.setInput(blob)
    detections = network.forward()

    face_roi = None
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_min:
            bbox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = bbox.astype("int")

            # sometimes if the face is closer to the edge of the capture area the detector can return negative values, and this will crash the execution.
            # the recommendation is to keep the face on center of the video, but just to guarantee, let's create this condition to prevent the program from crashing
            if (start_x<0 or start_y<0 or end_x > w or end_y > h):
                #print(start_y,end_y,start_x,end_x)
                continue

            face_roi = orig_frame[start_y:end_y,start_x:end_x]
            face_roi = cv2.resize(face_roi, (90, 120)) ## comment IF you don`t need to resize all faces to a fixed size
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # draw bounding box
            if show_conf:
                text_conf = "{:.2f}%".format(confidence * 100)
                cv2.putText(frame, text_conf, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    return frame, face_roi