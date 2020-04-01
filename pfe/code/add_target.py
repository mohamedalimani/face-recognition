import cv2, sys, os, time, shutil


def delay_start():
    time_passed = 6
    i = 0
    t1 = time.perf_counter()
    while i != time_passed:
        t2 = time.perf_counter()
        if t2-t1 > i:
            i += 1
            print(time_passed-i)


lbp_classifier_face = 'Data/lbpcascade_frontalface.xml'
target_dir = '../target'
(im_width, im_height) = (110, 90)
size = 1

lbp_cascade_face = cv2.CascadeClassifier(lbp_classifier_face)
camera = cv2.VideoCapture(0)
try:
    target_name = input("Donne le nom du personage que tu veut l'ajouter :\n")
except ValueError:
    print("Vous devez entrer un nom")
    sys.exit(0)
path = os.path.join(target_dir, target_name)
if not os.path.isdir(path):
    os.mkdir(path)

# Generate name for image file
pin = sorted([int(n[:n.find('.')]) for n in os.listdir(path) if n[0] != '.'] + [0])[-1] + 1

# Beginning message
print("\nLe programme va capturer 40 images. \
Deplacez votre tete pour augmenter la precision pendant le fonctionnement.\n")
delay_start()
# The program loops until it has 40 images of the face.
count = 0
pause = 0
t = 0
count_max = 40
while count < count_max:
    (working, frame) = camera.read()
    # Loop until the camera is working
    while not working:
        # Put the image from the camera into 'frame'
        (working, frame) = camera.read()
        if not working:
            print("Probleme avec la camera")
            time.sleep(1)
            t = t + 1
            if t == 3:
                print("probleme survenu le programme doit quitter !")
                sys.exit(0)

    # Get image size
    height, width, channels = frame.shape

    # Flip frame
    frame = cv2.flip(frame, 1, 0)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = lbp_cascade_face.detectMultiScale(gray)

    # We only consider largest face
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]

        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        # Draw rectangle and write name
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, '%s - %d/40' % (target_name, count), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0))

        # Remove false positives
        if w * 6 < width or h * 6 < height:
            print("Non claire")
        else:
            # To create diversity, only save every fith detected image
            if pause == 0:
                print("enregistrement de la capture " + str(count + 1) + "/" + str(count_max))

                # Save image file
                cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
                pin += 1
                count += 1
                pause = 1

    if pause > 0:
        pause = (pause + 1) % 3
    cv2.imshow('capture', frame)
    if cv2.waitKey(10) == 13:
        shutil.rmtree(path)
        print(f'{target_name} a été supprimé avec succées')
        exit()
camera.release()
cv2.destroyAllWindows()
