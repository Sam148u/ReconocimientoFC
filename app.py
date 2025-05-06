import tkinter as tk
from tkinter import messagebox
import register_face
import recognize_face
import database

# Funciones que se conectan con el backend
def registrar_rostro():
    def registrar():
        nombre = entry_nombre.get().strip()
        if nombre:
            ventana_nombre.destroy()
            register_face.main(nombre)
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingresa un nombre.")

    ventana_nombre = tk.Toplevel()
    ventana_nombre.title("Registrar Nuevo Rostro")
    ventana_nombre.geometry("300x150")

    tk.Label(ventana_nombre, text="Nombre del usuario:").pack(pady=10)
    entry_nombre = tk.Entry(ventana_nombre)
    entry_nombre.pack(pady=5)

    tk.Button(ventana_nombre, text="Registrar", command=registrar).pack(pady=10)

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

    # Crear ventana para seleccionar usuario
    eliminar_window = tk.Toplevel()
    eliminar_window.title("Eliminar Usuario")
    eliminar_window.geometry("300x200")

    tk.Label(eliminar_window, text="Selecciona un usuario a eliminar:").pack(pady=10)
    selected_user = tk.StringVar(eliminar_window)
    selected_user.set(nombres[0])  # valor por defecto

    drop = tk.OptionMenu(eliminar_window, selected_user, *nombres)
    drop.pack(pady=10)

    def confirmar_eliminacion():
        nombre = selected_user.get()
        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar a '{nombre}'?")
        if confirm:
            database.delete_user(nombre)
            messagebox.showinfo("Eliminado", f"Usuario '{nombre}' eliminado exitosamente.")
            eliminar_window.destroy()

    tk.Button(eliminar_window, text="Eliminar", command=confirmar_eliminacion).pack(pady=10)
# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.geometry("400x350")

# Botones
tk.Label(root, text="Reconocimiento Facial", font=("Helvetica", 16)).pack(pady=20)

tk.Button(root, text="Registrar Rostro", width=25, command=registrar_rostro).pack(pady=10)
tk.Button(root, text="Reconocer Rostro", width=25, command=reconocer_rostro).pack(pady=10)
tk.Button(root, text="Ver Registros Guardados", width=25, command=ver_registros).pack(pady=10)
tk.Button(root, text="Eliminar Usuario", width=25, command=eliminar_usuario).pack(pady=10)
tk.Button(root, text="Salir", width=25, command=root.quit).pack(pady=20)

root.mainloop()
