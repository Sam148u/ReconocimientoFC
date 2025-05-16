import customtkinter as ctk
import register_face
import recognize_face
import database
from tkinter import messagebox

# Estilo global
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("dark-blue")  # Tema base

# Ventana principal
root = ctk.CTk()
root.title("Reconocimiento Facial")
root.geometry("350x400")
root.resizable(False, False)

# Fondo con imagen (degradado o formas futuristas)
from PIL import Image

image = Image.open("S:\\reconocimiento_facial\\fondo.png")
bg_image = ctk.CTkImage(dark_image=image, size=(350, 400))

bg_label = ctk.CTkLabel(root, image=bg_image, text="")
bg_label.place(x=0, y=0)

# Panel de control (estilo tarjeta)
frame = ctk.CTkFrame(root, width=350, height=400, corner_radius=15)
frame.place(x=40, y=30)

title = ctk.CTkLabel(frame, text=" Sistema de Reconocimiento ", font=("Segoe UI", 20, "bold"))
title.pack(pady=(10, 10))

def registrar_rostro():
    def registrar():
        nombre = entry_nombre.get().strip()
        if nombre:
            ventana_nombre.destroy()
            register_face.main(nombre)
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingresa un nombre.")

    ventana_nombre = ctk.CTkToplevel(root)
    ventana_nombre.geometry("300x150")
    ventana_nombre.title("Registrar Nuevo Rostro")

    ctk.CTkLabel(ventana_nombre, text="Nombre del usuario:").pack(pady=10)
    entry_nombre = ctk.CTkEntry(ventana_nombre)
    entry_nombre.pack(pady=5)
    ctk.CTkButton(ventana_nombre, text="Registrar", command=registrar).pack(pady=10)

def reconocer_rostro():
    recognize_face.main()

def ver_registros():
    users = database.get_all_users()
    nombres = "\n".join([u[0] for u in users])
    messagebox.showinfo("Rostros Registrados", nombres if nombres else "No hay registros.")

def eliminar_usuario():
    users = database.get_all_users()
    nombres = [u[0] for u in users]

    if not nombres:
        messagebox.showinfo("Eliminar Usuario", "No hay usuarios registrados.")
        return

    eliminar_window = ctk.CTkToplevel(root)
    eliminar_window.title("Eliminar Usuario")
    eliminar_window.geometry("300x200")

    ctk.CTkLabel(eliminar_window, text="Selecciona un usuario:").pack(pady=10)
    selected_user = ctk.StringVar(value=nombres[0])
    drop = ctk.CTkOptionMenu(eliminar_window, variable=selected_user, values=nombres)
    drop.pack(pady=10)

    def confirmar_eliminacion():
        nombre = selected_user.get()
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar a '{nombre}'?")
        if confirm:
            database.delete_user(nombre)
            messagebox.showinfo("Eliminado", f"Usuario '{nombre}' eliminado.")
            eliminar_window.destroy()

    ctk.CTkButton(eliminar_window, text="Eliminar", command=confirmar_eliminacion).pack(pady=10)

# Botones
ctk.CTkButton(frame, text="Registrar Rostro", width=200, command=registrar_rostro).pack(pady=10)
ctk.CTkButton(frame, text="Reconocer Rostro", width=200, command=reconocer_rostro).pack(pady=10)
ctk.CTkButton(frame, text="Ver Registros", width=200, command=ver_registros).pack(pady=10)
ctk.CTkButton(frame, text="Eliminar Usuario", width=200, command=eliminar_usuario).pack(pady=10)
ctk.CTkButton(frame, text="Salir", width=200, command=root.quit).pack(pady=20)

root.mainloop()
