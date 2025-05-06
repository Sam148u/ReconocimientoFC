# recognize_face.py
import face_recognition
import cv2
import database
import numpy as np
import tkinter as tk
from tkinter import messagebox

def main():
    # Cargar usuarios registrados
    users = database.get_all_users()
    known_names = []
    known_encodings = []

    for name, encoding_blob in users:
        known_names.append(name)
        known_encodings.append(np.frombuffer(encoding_blob, dtype=np.float64))

    # Abrir la cámara
    video_capture = cv2.VideoCapture(0)
    recognized = set()  # Para evitar múltiples popups para la misma persona

    print("Reconociendo... Presiona 'q' para salir.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Desconocido"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            # Mostrar ventana emergente si no se ha reconocido aún en esta sesión
            if name != "Desconocido" and name not in recognized:
                recognized.add(name)
                root = tk.Tk()
                root.withdraw()  # Oculta ventana principal
                messagebox.showinfo("Persona Reconocida", f"Hola, {name} 👋")
                root.destroy()

            # Dibujar recuadro con el nombre
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # Mostrar mensaje de salida en la esquina inferior
            cv2.putText(
                frame,
                "Presiona 'q' para salir",
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )
    

        cv2.imshow('Reconocimiento Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
