# Hasznalat
# Ha laptopon, PC-n vagy GPU-n kodol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# Ha Raspberry Pi-n kodol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# A szukseges csomagok importalasa
import face_recognition
import argparse
import pickle
import cv2
import os

# Az argument parser konstrualasa
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# Kiragadja az input kepek eleresi utjat az adatbazisbol 
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# Inicializalja az ismert kodok es az ismert nevek listajat
knownEncodings = []
knownNames = []

# Lepteti a kep eleresi utjat
for (i, imagePath) in enumerate(imagePaths):
	# Kitorli a szemely nevet a kep eleresi utjabol
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# Betolti az input kepet + RGB konvertalas
	# dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detektalja a hatarolok (x, y) koordinatait
	# Osszehasonlit minden arcot az input keppel 
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# Kiszamitja az arc korvonalait az arcon
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Lepteti a kodokat
	for encoding in encodings:
		# Hozzaad minden kodot es nevet az adatbazishoz 			
		knownEncodings.append(encoding)
		knownNames.append(name)

# Leirja az arci kodokat es neveket a lemezre 
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()