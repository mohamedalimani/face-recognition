import cv2
import time
import numpy as np
import concurrent.futures
import pickle

ret = True
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")


with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k, v in og_labels.items()}

print("enter 0 if you want to open webcam ", end='\n')
vid_name = input("enter video name (with it's extension) ...\n")
if vid_name == '0':
    vid_dir = int(vid_name)
else:
    vid_dir = "../ressources/" + vid_name
vid = cv2.VideoCapture(vid_dir)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
frameCount = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
frameHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameWidth = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame = np.empty((1, frameHeight, frameWidth, 3), np.dtype('uint8'))


def read_frame(fr, re):
    re, fr = vid.read()
    return re, fr


loop_count = 0
t1 = time.perf_counter()
while ret:
    loop_count += 1
    with concurrent.futures.ThreadPoolExecutor() as executor:
        read_task = executor.submit(read_frame, frame, ret)
        ret, frame = read_task.result()
        cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame is not None:
        face = face_cascade.detectMultiScale(cvt_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in face:
            # recognize me
            gray_face_only = cvt_frame[y:y + h, x:x + w]
            color_face_only = frame[y:y+h, x:x+w]
            cv2.imwrite("8.jpg", color_face_only)
            id_, conf = recognizer.predict(gray_face_only)
            if 45 <= conf:
                font = cv2.putText(frame,
                                   labels[id_],
                                   (x, y+h+30),
                                   cv2.FONT_HERSHEY_SIMPLEX,
                                   1,
                                   (255, 255, 255),
                                   3,
                                   cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        resized = cv2.resize(frame, (450, 450), interpolation=cv2.INTER_AREA)
        cv2.imshow("video ", resized)
        if cv2.waitKey(1) == 13:
            break
t2 = time.perf_counter()
print(f'{round(t2-t1,2)} seconds passed')
print(loop_count//round(t2-t1, 2))
vid.release()
cv2.destroyAllWindows()

