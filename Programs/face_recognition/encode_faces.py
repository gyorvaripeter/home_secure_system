# Haszn�lat
# Ha laptopon, PC-n vagy GPU-n k�dol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# Ha Raspberry Pi-n k�dol:
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# A sz�ks�ges csomagok import�l�sa
import face_recognition
import argparse
import pickle
import cv2
import os

# Az argument parser konstru�l�sa
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# Kiragadja az input k�pek el�r�si �tj�t az adatb�zisb�l 
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# Inicializ�lja az ismert k�dok �s az ismert nevek list�j�t
knownEncodings = []
knownNames = []

# L�pteti a k�p el�r�si �tj�t
for (i, imagePath) in enumerate(imagePaths):
	# Kit�rli a szem�ly nev�t a k�p el�r�si �tj�b�l
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# Bet�lti az input k�pet + RGB konvert�l�s
	# dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detekt�lja a hat�rol�k (x, y) koordin�t�it
	# �sszehasonl�t minden arcot az input k�ppel 
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# Kisz�m�tja az arc k�rvonalait az arcon
	encodings = face_recognition.face_encodings(rgb, boxes)

	# L�pteti a k�dokat
	for encoding in encodings:
		# Hozz�ad minden k�dot �s nevet az adatb�zishoz 			knownEncodings.append(encoding)
		knownNames.append(name)

# Le�rja az arci k�dokat �s neveket a lemezre 
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()