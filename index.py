# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from threading import Thread
# from PIL import Image, ImageTk
# import random

# class VideoDetectionApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Object Detection with YOLO")
#         self.root.geometry("800x600")

#         self.video_path = ""
#         self.image_path = ""
#         self.cap = None
#         self.running = False

#         self.create_widgets()
#         self.load_yolo()

#     def create_widgets(self):
#         # Frame for buttons
#         main_button_frame = tk.Frame(self.root)
#         main_button_frame.pack(pady=10)

#         self.realtime_button = tk.Button(main_button_frame, text="Detection en Temps Réel", command=self.start_realtime_detection, width=20)
#         self.realtime_button.grid(row=0, column=0, padx=5)

#         self.select_video_button = tk.Button(main_button_frame, text="Choisir Vidéo depuis PC", command=self.open_video_file, width=20)
#         self.select_video_button.grid(row=0, column=1, padx=5)

#         self.select_image_button = tk.Button(main_button_frame, text="Choisir Image depuis PC", command=self.open_image_file, width=20)
#         self.select_image_button.grid(row=0, column=2, padx=5)

#         self.start_button = tk.Button(main_button_frame, text="Début de Détection", state="disabled", command=self.start_detection, width=20)
#         self.start_button.grid(row=1, column=0, padx=5, pady=5)

#         self.stop_button = tk.Button(main_button_frame, text="Stop Détection", state="disabled", command=self.stop_detection, width=20)
#         self.stop_button.grid(row=1, column=1, padx=5, pady=5)

#         self.quit_button = tk.Button(main_button_frame, text="Fin", command=self.quit_program, width=20)
#         self.quit_button.grid(row=1, column=2, padx=5, pady=5)

#         # Label for video display
#         self.video_label = tk.Label(self.root)
#         self.video_label.pack(pady=10)

#     def load_yolo(self):
#         self.net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
#         self.layer_names = self.net.getLayerNames()
#         self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
#         self.classes = []
#         with open("coco.names", "r") as f:
#             self.classes = [line.strip() for line in f.readlines()]

#         # Generate random colors for each class
#         self.colors = {class_name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for class_name in self.classes}

#     def open_video_file(self):
#         self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
#         if self.video_path:
#             self.image_path = ""
#             self.realtime_button.config(state="disabled")
#             self.select_image_button.config(state="disabled")
#             self.start_button.config(state="normal")
#             self.stop_button.config(state="normal")
#             messagebox.showinfo("Vidéo Sélectionnée", f"Vidéo sélectionnée : {self.video_path}")

#     def open_image_file(self):
#         self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
#         if self.image_path:
#             self.video_path = ""
#             self.realtime_button.config(state="disabled")
#             self.select_video_button.config(state="disabled")
#             self.start_button.config(state="normal")
#             self.stop_button.config(state="disabled")
#             messagebox.showinfo("Image Sélectionnée", f"Image sélectionnée : {self.image_path}")

#     def start_realtime_detection(self):
#         self.video_path = 0  # Use the webcam
#         self.image_path = ""
#         self.select_video_button.config(state="disabled")
#         self.select_image_button.config(state="disabled")
#         self.start_button.config(state="normal")
#         self.stop_button.config(state="normal")

#     def start_detection(self):
#         self.start_button.config(state="disabled")
#         self.stop_button.config(state="normal")
#         self.running = True
#         if self.image_path:
#             self.process_image()
#         else:
#             self.detection_thread = Thread(target=self.process_video)
#             self.detection_thread.start()

#     def process_image(self):
#         image = cv2.imread(self.image_path)
#         self.detect_and_display(image)

#     def process_video(self):
#         self.cap = cv2.VideoCapture(self.video_path)
#         while self.cap.isOpened() and self.running:
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
#             # Resize frame for faster processing
#             frame = cv2.resize(frame, (640, 480))
#             self.detect_and_display(frame)
#         self.cap.release()
#         self.stop_detection()

#     def detect_and_display(self, frame):
#         height, width, channels = frame.shape
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         self.net.setInput(blob)
#         outs = self.net.forward(self.output_layers)

#         class_ids = []
#         confidences = []
#         boxes = []

#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)

#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

#         for i in range(len(boxes)):
#             if i in indexes:
#                 x, y, w, h = boxes[i]
#                 label = str(self.classes[class_ids[i]])
#                 color = self.colors[label]
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame_resized = cv2.resize(frame_rgb, (800, 450))  # Adjust the resolution for display
#         img = Image.fromarray(frame_resized)
#         imgtk = ImageTk.PhotoImage(image=img)
#         self.video_label.imgtk = imgtk
#         self.video_label.config(image=imgtk)

#     def stop_detection(self):
#         self.running = False
#         if self.cap:
#             self.cap.release()
#         cv2.destroyAllWindows()
#         self.stop_button.config(state="disabled")
#         self.start_button.config(state="normal")
#         self.realtime_button.config(state="normal")
#         self.select_video_button.config(state="normal")
#         self.select_image_button.config(state="normal")

#     def quit_program(self):
#         self.running = False
#         if self.cap:
#             self.cap.release()
#         self.root.quit()
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VideoDetectionApp(root)
#     root.mainloop()
