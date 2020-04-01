import cv2, time, concurrent.futures, pickle, os
import numpy as np

ret = True
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Data/trainer.yml")

# lire le fichier labels qui contient les label et ID des personnages dans le fichier "target"

with open("Data/labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k, v in og_labels.items()}

# entrée du nom du video ou si l'utilisateur veut utilisé le webcam

vid_name = "unknown.mp4"
files2 = []
vid_dir = "unknown"
print("\ntapez 0 si vous voulez ouvrir le webcam ou entrer le nom du video ...", end='\n\n')
for (root, directories, files) in os.walk("../ressources/"):
    files2 = files
    files2.append("0")
    print(files[:-1])
while vid_name not in files2:
    vid_name = input()
    if vid_name == '0':
        vid_dir = int(vid_name)
    else:
        if vid_name.find(".") == -1:
            vid_name = vid_name + ".mp4"
        print(f"le nom du video que tu viens de tapez n'existe pas ! reessayer avec ces noms ou  \n {files2[:-1]}"
              f" ou tapez 0 si vous voulez ouvrir le webcam")
        vid_dir = "../ressources/" + vid_name

vid = cv2.VideoCapture(vid_dir)
face_cascade = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")
frameCount = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
frameHeight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameWidth = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame = np.empty((1, frameHeight, frameWidth, 3), np.dtype('uint8'))


def read_frame(fr, re):
    re, fr = vid.read()
    return re, fr


t1 = time.perf_counter()
while ret:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        read_task = executor.submit(read_frame, frame, ret)
        ret, frame = read_task.result()
    if frame is not None:
        cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(cvt_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in face:
            # recognize me
            gray_face_only = cvt_frame[y:y + h, x:x + w]
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
print(f'finished {round(t2-t1,2)} seconds')
vid.release()
cv2.destroyAllWindows()

