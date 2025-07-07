import cv2
import numpy as np
import os
import time
import pygame
from picamera2 import Picamera2
from libcamera import Transform

time.sleep(2)

# Ses
AUDIO_DIR = "nesneler"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Türkçe sınıf çevirileri
turkish_classes = {
    "person": "insan",
    "bicycle": "bisiklet",
    "car": "araba",
    "motorbike": "motosiklet",
    "bus": "otobus",
    "truck": "tir",
    "traffic light": "trafik isigi",
    "stop sign": "dur isareti",
    "bench": "bank",
    "dog": "kopek",
    "horse": "at",
    "bottle": "sise",
    "chair": "sandalye",
    "sofa": "kanepe",
    "bed": "yatak",
    "laptop": "dizustu bilgisayar",
    "cell phone": "cep telefonu",
    "cat": "kedi"
}

def normalize_filename(text):
    return text.lower().replace(" ", "_")

pygame.init()
pygame.mixer.init()

def speak(text, speech_cache):
    try:
        filename = normalize_filename(text) + ".mp3"
        full_path = os.path.join(AUDIO_DIR, filename)
        if os.path.exists(full_path):
            if text not in speech_cache:
                speech_cache[text] = full_path
            pygame.mixer.music.load(speech_cache[text])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        else:
            print(f"Uyari: '{text}' sesi bulunamadi. Devam ediliyor...")
    except Exception as e:
        print(f"Sesli bildirim hatasi: {e}")

# Sınıf isimlerini oku
with open("/home/pi/Desktop/yolo/coco.names", "r") as f:
    classes_en = [line.strip() for line in f.readlines()]
selected_classes = list(turkish_classes.keys())

# YOLO modelini yükle
net = cv2.dnn.readNet("/home/pi/Desktop/yolo/yolov3.weights", "/home/pi/Desktop/yolo/yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Kamera başlat
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}, transform=Transform(hflip=1)))
picam2.start()

last_spoken = ""
last_time_spoken = 0
speech_cache = {}

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    height, width, _ = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes_en[class_id] in selected_classes:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    largest_object = None
    largest_area = 0

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes_en[class_ids[i]])
            area = w * h
            if area > largest_area:
                largest_area = area
                largest_object = label

    if largest_object:
        spoken_label_tr = turkish_classes.get(largest_object, largest_object)
        current_time = time.time()
        if spoken_label_tr != last_spoken or (current_time - last_time_spoken) >= 2:
            speak(f"{spoken_label_tr} algilandi", speech_cache)
            last_spoken = spoken_label_tr
            last_time_spoken = current_time

    # Görüntü gösterimi devre dışı bırakıldı
    # cv2.imshow("YOLOv3 Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
