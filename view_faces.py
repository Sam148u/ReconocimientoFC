import database

# Obtener todos los usuarios registrados
users = database.get_all_users()

# Ver los resultados
if users:
    print("Usuarios registrados:")
    for user in users:
        name, encoding = user
        print(f"Nombre: {name}")
else:
    print("No hay usuarios registrados.")
