import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from PIL import Image, ImageTk
import cv2
from app.yolo import YOLO
from app.gui import create_widgets

class VideoDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection with YOLO")
        self.root.geometry("800x600")

        self.video_path = ""
        self.image_path = ""
        self.cap = None
        self.running = False

        self.yolo = YOLO()
        self.create_widgets()

    def create_widgets(self):
        create_widgets(self)

    def open_video_file(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if self.video_path:
            self.image_path = ""
            self.realtime_button.config(state="disabled")
            self.select_image_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.stop_button.config(state="normal")
            messagebox.showinfo("Vidéo Sélectionnée", f"Vidéo sélectionnée : {self.video_path}")

    def open_image_file(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if self.image_path:
            self.video_path = ""
            self.realtime_button.config(state="disabled")
            self.select_video_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            messagebox.showinfo("Image Sélectionnée", f"Image sélectionnée : {self.image_path}")

    def start_realtime_detection(self):
        self.video_path = 0  # Use the webcam
        self.image_path = ""
        self.select_video_button.config(state="disabled")
        self.select_image_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.stop_button.config(state="normal")

    def start_detection(self):
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.running = True
        if self.image_path:
            self.process_image()
        else:
            self.detection_thread = Thread(target=self.process_video)
            self.detection_thread.start()

    def process_image(self):
        image = cv2.imread(self.image_path)
        self.detect_and_display(image)

    def process_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        while self.cap.isOpened() and self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            # Resize frame for faster processing
            frame = cv2.resize(frame, (640, 480))
            self.detect_and_display(frame)
        self.cap.release()
        self.stop_detection()

    def detect_and_display(self, frame):
        detections = self.yolo.detect_objects(frame)
        frame = self.yolo.draw_boxes(frame, detections)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (800, 450))  # Adjust the resolution for display
        img = Image.fromarray(frame_resized)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.realtime_button.config(state="normal")
        self.select_video_button.config(state="normal")
        self.select_image_button.config(state="normal")

    def quit_program(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.quit()
        self.root.destroy()
