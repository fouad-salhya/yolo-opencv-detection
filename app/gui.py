import tkinter as tk

def create_widgets(app):
    # Frame for buttons
    main_button_frame = tk.Frame(app.root)
    main_button_frame.pack(pady=10)

    app.realtime_button = tk.Button(main_button_frame, text="Detection en Temps Réel", command=app.start_realtime_detection, width=20)
    app.realtime_button.grid(row=0, column=0, padx=5)

    app.select_video_button = tk.Button(main_button_frame, text="Choisir Vidéo depuis PC", command=app.open_video_file, width=20)
    app.select_video_button.grid(row=0, column=1, padx=5)

    app.select_image_button = tk.Button(main_button_frame, text="Choisir Image depuis PC", command=app.open_image_file, width=20)
    app.select_image_button.grid(row=0, column=2, padx=5)

    app.start_button = tk.Button(main_button_frame, text="Début de Détection", state="disabled", command=app.start_detection, width=20)
    app.start_button.grid(row=1, column=0, padx=5, pady=5)

    app.stop_button = tk.Button(main_button_frame, text="Stop Détection", state="disabled", command=app.stop_detection, width=20)
    app.stop_button.grid(row=1, column=1, padx=5, pady=5)

    app.quit_button = tk.Button(main_button_frame, text="Fin", command=app.quit_program, width=20)
    app.quit_button.grid(row=1, column=2, padx=5, pady=5)

    # Label for video display
    app.video_label = tk.Label(app.root)
    app.video_label.pack(pady=10)
