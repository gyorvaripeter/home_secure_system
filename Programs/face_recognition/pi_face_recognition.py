# Terminal parancs az indításhoz
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# szükséges csomagok importálása
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
from gpiozero import LED
#  argumentumparser-ral felépíteni a parncskiadást
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# feltöltenia már ismert arcokkal és beágyazni az OpenCV számára 
# (haircascade az arc detektáláshoz)
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# Iniciálja a streamet és elindítja a kamera bemelegítését.
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start() <--webkamerához ez kell
vs = VideoStream(usePiCamera=True).start()

time.sleep(2.0)
led1 = LED(17)
led2= LED(27)
# fps számláló
fps = FPS().start()

# lépked a képkockákon a streamelt videó fájlból
while True:
    # visszaveszi a minőséget a gyorsabb feldolgozás érdekében
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # átkonvertálja a bemenő képkockát (1) BGR-ből greyscale-re az arc
    # detektáláshoz és (2) BGR-ből RGB-re (az arc felismeréshez)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # arcdetektálás a greyscale kockákból
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # az OpenCV viszzadja értékül a keret koordinátáit (x,y,w,h)ben
    # de ezeken belül szükség van(top,right,bottom,left) adatokra,szóval
    # szükség van az újra hozzárendelésre
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # kiszámítja az arcvonások értékeit minden egyes dobozra
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # lépked az arcvonásokon
    for encoding in encodings:
        # megpróbál minden egyes fejet egyeztetni az input képekből
        # az átkódoltakkal
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"
        
        # hogy ha talál egyezést
        if True in matches:
            # megtalálja az archoz rendelt indexeket és inicializál
            # egy szótárat  
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            
            # lépked az indexelt találatokon és ad egy számot
            # minden egyes felismert archoz
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                
            # meghatározza a felismertarcok legbővebb halmazát
            name = max(counts, key=counts.get)
            led1.on()
            time.sleep(3)
            led1.off()
        # a név lista frissitése
        names.append(name)
        if name=="Unknown" :  
            led2.on()
            time.sleep(3)
            led2.off()
    # léptetés a felismert arcokon
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # keret rajzolás a fej köré és név kiírása
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)

    # megjeleníti a képet a képernyőn
    cv2.imshow("Frame", frame)
    cv2.flip(frame,1)
    key = cv2.waitKey(1) & 0xFF

    # ha a q-gomb lenyomásra kerül befejeződik a folyamat
    if key == ord("q"):
        led.off()
        break

    # fps számláló frissítés
    fps.update()

# időzítő és az fps számláló megállítása, kiírása
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# egy kis tisztítás
cv2.destroyAllWindows()
vs.stop()