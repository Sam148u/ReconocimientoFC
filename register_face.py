# register_face.py
import face_recognition
import cv2
import database
import numpy as np

def main(nombre):
    database.create_database()

    video_capture = cv2.VideoCapture(0)

    print(f"Posiciona tu rostro en la cámara y presiona 's' para registrar a {nombre}.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("No se pudo obtener una imagen de la cámara. Intenta de nuevo.")
            break

        # Mostrar mensaje en la ventana de la cámara
        mensaje = f"Presiona 's' para capturar rostro de {nombre}"
        cv2.putText(frame, mensaje, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Registrar Rostro', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                encoding_bytes = encoding.tobytes()
                database.insert_user(nombre, encoding_bytes)
                print(f"{nombre} registrado exitosamente.")
            else:
                print("No se detectó ningún rostro. Intenta de nuevo.")
            break

    video_capture.release()
    cv2.destroyAllWindows()




