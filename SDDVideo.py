


from PyQt5 import QtCore, QtGui, QtWidgets

from pyimagesearch import social_distancing_config as config
from pyimagesearch.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import os
import cv2

class Ui_SDDVideo(object):

    def browse_file(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        print(fileName)
        self.lineEdit.setText(fileName)

    def sdd_video(self):

        try:
            video = self.lineEdit.text()
            if video == "" or video == "null":
                self.showMessageBox("Information", "Please fill out  fields")

            else:
                # load the COCO class labels our YOLO model was trained on
                labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
                LABELS = open(labelsPath).read().strip().split("\n")

                # derive the paths to the YOLO weights and model configuration
                weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
                configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

                # load our YOLO object detector trained on COCO dataset (80 classes)
                print("[INFO] loading YOLO from disk...")
                net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

                # determine only the *output* layer names that we need from YOLO
                ln = net.getLayerNames()
                ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

                cap = cv2.VideoCapture(video)
                writer = None
                cnt = 0
                (grabbed, frame) = cap.read()
                print(str(len(frame))+"frames")
                # loop over the frames from the video stream
                while True:
                    # read the next frame from the file
                    (grabbed, frame) = cap.read()
                    cnt = cnt + 1
                    print("frame" + str(cnt))

                    # if the frame was not grabbed, then we have reached the end
                    # of the stream
                    if not grabbed:
                        break

                    # resize the frame and then detect people (and only people) in it
                    frame = imutils.resize(frame, width=700)
                    results = detect_people(frame, net, ln,
                                            personIdx=LABELS.index("person"))

                    # initialize the set of indexes that violate the minimum social
                    # distance
                    violate = set()

                    # ensure there are *at least* two people detections (required in
                    # order to compute our pairwise distance maps)
                    if len(results) >= 2:
                        # extract all centroids from the results and compute the
                        # Euclidean distances between all pairs of the centroids
                        centroids = np.array([r[2] for r in results])
                        D = dist.cdist(centroids, centroids, metric="euclidean")

                        # loop over the upper triangular of the distance matrix
                        for i in range(0, D.shape[0]):
                            for j in range(i + 1, D.shape[1]):
                                # check to see if the distance between any two
                                # centroid pairs is less than the configured number
                                # of pixels
                                if D[i, j] < config.MIN_DISTANCE:
                                    # update our violation set with the indexes of
                                    # the centroid pairs
                                    violate.add(i)
                                    violate.add(j)

                    # loop over the results
                    for (i, (prob, bbox, centroid)) in enumerate(results):
                        # extract the bounding box and centroid coordinates, then
                        # initialize the color of the annotation
                        (startX, startY, endX, endY) = bbox
                        (cX, cY) = centroid
                        color = (0, 255, 0)

                        # if the index pair exists within the violation set, then
                        # update the color
                        if i in violate:
                            color = (0, 0, 255)

                        # draw (1) a bounding box around the person and (2) the
                        # centroid coordinates of the person,
                        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                        cv2.circle(frame, (cX, cY), 5, color, 1)

                    # draw the total number of social distancing violations on the
                    # output frame
                    text = "Social Distancing Violations: {}".format(len(violate))
                    cv2.putText(frame, text, (10, frame.shape[0] - 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break

                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter('output.avi', fourcc, 25,
                                             (frame.shape[1], frame.shape[0]), True)

                    # if the video writer is not None, write the frame to the output
                    # video file
                    if writer is not None:
                        writer.write(frame)
        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
            print(e)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(712, 433)
        Dialog.setStyleSheet("background-color: rgb(89, 26, 41);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(160, 60, 461, 61))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 18pt \"Georgia\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(150, 150, 191, 41))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Georgia\";")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(150, 200, 341, 41))
        self.lineEdit.setStyleSheet("font: 14pt \"Times New Roman\";")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(530, 200, 121, 41))
        self.pushButton.setStyleSheet("color: rgb(0, 85, 127);\n"
"font: 14pt \"Times New Roman\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.browse_file)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 280, 131, 41))
        self.pushButton_2.setStyleSheet("font: 14pt \"Georgia\";\n"
"background-color: rgb(85, 85, 127);\n"
"color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.sdd_video)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Social Distance Detection with Video"))
        self.label_2.setText(_translate("Dialog", "Select Video"))
        self.pushButton.setText(_translate("Dialog", "Browse"))
        self.pushButton_2.setText(_translate("Dialog", "Detect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
