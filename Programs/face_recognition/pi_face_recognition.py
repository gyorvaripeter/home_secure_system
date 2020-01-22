# Terminal parancs az inditashoz
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# szukseges csomagok importalasa
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
from gpiozero import LED
#  argumentumparser-ral felepiteni a parncskiadast
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# feltoltenia mar ismert arcokkal es beagyazni az OpenCV szamara 
# (haircascade az arc detektalashoz)
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# Inicialja a streamet es elinditja a kamera bemelegiteset
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start() <--webkamerahoz ez kell
vs = VideoStream(usePiCamera=True, rotation = 180, sensor_mode = 2).start()

known = False
time.sleep(2.0)
led1 = LED(17)
led2= LED(27)
# fps szamlalo
fps = FPS().start()

# lepked a kepkockakon a streamelt video fajlbol
while True:
    # visszaveszi a minoseget a gyorsabb feldolgozas erdekeben
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # atkonvertalja a bemeno kepkockat (1) BGR-bol greyscale-re az arc
    # detektalashoz es (2) BGR-bol RGB-re (az arc felismereshez)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # arcdetektalas a greyscale kockakbol
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # az OpenCV viszzadja ertekul a keret koordinatait (x,y,w,h)ben
    # de ezeken belul szukseg van(top,right,bottom,left) adatokra,szoval
    # szukseg van az ujra hozzarendelesre
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # kiszamitja az arcvonasok ertekeit minden egyes dobozra
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # lepked az arcvonasokon
    for encoding in encodings:
        # megprobal minden egyes fejet egyeztetni az input kepekbol
        # az atkodoltakkal
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"
        
        # hogy ha talal egyezest
        if True in matches:
            # megtalalja az archoz rendelt indexeket es inicializal
            # egy szotarat  
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            
            # lepked az indexelt talalatokon es ad egy szamot
            # minden egyes felismert archoz
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                
            # meghatarozza a felismertarcok legbovebb halmazat
            name = max(counts, key=counts.get)
            
        # a nev lista frissitese
        names.append(name)
        
        #zarak nyitasa, zarva hagyas imitalasa ledekkel
        if name=="Unknown" :  
            led2.on()
            time.sleep(2)
            led2.off()
        else:
            led1.on()
            time.sleep(2)
            led1.off()
            known = True
        
    # leptetes a felismert arcokon
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # keret rajzolas a fej kore es nev kiirasa
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)

    # megjeleniti a kepet a kepernyon
    cv2.imshow("Frame", frame)

    # ha felismert vagy ismeretlen akkor kilep
    if known:
        # fps szamlalo frissites
        fps.update()

        # idozito es az fps szamlalo megallitasa, kiirasa
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # egy kis tisztitas
        cv2.destroyAllWindows()
        vs.stop()
        break

    