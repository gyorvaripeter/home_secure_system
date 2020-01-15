# Használat
# Ha laptopon, PC-n vagy GPU-n kódol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# Ha Raspberry Pi-n kódol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# A szükséges csomagok importálása
import face_recognition
import argparse
import pickle
import cv2
import os

# Az argument parser konstruálása
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# Kiragadja az input képek elérési útját az adatbázisból 
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# Inicializálja az ismert kódok és az ismert nevek listáját
knownEncodings = []
knownNames = []

# Lépteti a kép elérési útját
for (i, imagePath) in enumerate(imagePaths):
	# Kitörli a személy nevét a kép elérési útjából
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# Betölti az input képet + RGB konvertálás
	# dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detektálja a határolók (x, y) koordinátáit
	# Összehasonlít minden arcot az input képpel 
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# Kiszámítja az arc körvonalait az arcon
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Lépteti a kódokat
	for encoding in encodings:
		# Hozzáad minden kódot és nevet az adatbázishoz 			knownEncodings.append(encoding)
		knownNames.append(name)

# Leírja az arci kódokat és neveket a lemezre 
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()