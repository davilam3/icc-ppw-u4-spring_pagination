import requests
import random
import time

BASE_URL = "http://localhost:8080/api"

API_USERS = f"http://localhost:8080/api/users"
API_CATEGORIES = f"http://localhost:8080/api/categories"
API_PRODUCTS = f"http://localhost:8080/api/products"

# =============================
# CONFIGURACIÓN
# =============================
TOTAL_USERS = 5
TOTAL_CATEGORIES = 8
TOTAL_PRODUCTS = 1000

# =============================
# DATOS BUSCABLES
# =============================
ADJECTIVES = ["Gamer", "Pro", "Ultra", "Smart", "Advanced", "Portable", "Max"]
PRODUCT_TYPES = ["Laptop", "Mouse", "Keyboard", "Monitor", "Tablet", "Phone", "Headset"]
BRANDS = ["Lenovo", "HP", "Dell", "Asus", "Samsung", "Logitech", "Apple"]
SPECS = ["i5", "i7", "Ryzen7", "16GB", "32GB", "512GB", "1TB"]

# =============================
# CREAR USUARIOS (PERSONALIZADO)
# =============================
def create_users():
    print("Creando usuarios...")
    user_ids = []

    # Lista fija de nombres completos
    full_names = [
        "Diana Avila",
        "Sebastian Cabrera",
        "Claudia Quevedo",
        "Valeria Mantilla",
        "Leonel Messi"
    ]

    for full_name in full_names:

        # Separamos nombre y apellido
        parts = full_name.split()
        first_name = parts[0]
        last_name = parts[1]

        # Construimos el email sin espacios y en minúsculas
        email = f"{first_name.lower()}{last_name.lower()}@test.com"

        data = {
            "name": full_name,
            "email": email,
            "password": "Password123"
        }

        r = requests.post(API_USERS, json=data)

        if r.status_code in [200, 201]:
            user_ids.append(r.json()["id"])
            print(f"Usuario creado: {full_name} - {email}")
        else:
            print("Error usuario:", r.status_code, r.text)

    return user_ids


# =============================
# CREAR CATEGORÍAS (FIJAS)
# =============================
def create_categories():
    print("Creando categorías...")
    category_ids = {}

    categories = [
        {"name": "Laptops", "description": "Computadoras portátiles"},
        {"name": "Smartphones", "description": "Teléfonos inteligentes"},
        {"name": "Accesorios", "description": "Mouse, teclados y periféricos"},
        {"name": "Monitores", "description": "Pantallas y monitores"},
        {"name": "Redes", "description": "Equipos de red y conectividad"},
        {"name": "Gaming", "description": "Equipos para videojuegos"},
    ]

    for cat in categories:
        r = requests.post(API_CATEGORIES, json=cat)

        if r.status_code in [200, 201]:
            cat_id = r.json()["id"]
            category_ids[cat["name"]] = cat_id
            print(f"Categoría creada: {cat['name']}")
        else:
            print("Error categoría:", r.status_code, r.text)

    return category_ids



# =============================
# GENERAR NOMBRE BUSCABLE
# =============================
def generate_product_name():
    return f"{random.choice(PRODUCT_TYPES)} {random.choice(ADJECTIVES)} {random.choice(BRANDS)} {random.choice(SPECS)}"


# =============================
# CREAR PRODUCTOS CON 2 CATEGORÍAS
# =============================
def create_products(user_ids, category_dict):
    print("Creando productos...")

    success = 0

    while success < TOTAL_PRODUCTS:

        # Elegimos categoría principal
        category_name = random.choice(list(category_dict.keys()))
        category_id_1 = category_dict[category_name]

        # Generar producto según categoría principal
        if category_name == "Laptops":
            name = f"Laptop {random.choice(BRANDS)} {random.choice(SPECS)}"
            related_categories = ["Gaming"]

        elif category_name == "Smartphones":
            name = f"Smartphone {random.choice(BRANDS)} 128GB"
            related_categories = ["Accesorios"]

        elif category_name == "Accesorios":
            name = f"{random.choice(['Mouse', 'Teclado', 'Headset'])} {random.choice(BRANDS)}"
            related_categories = ["Gaming"]

        elif category_name == "Monitores":
            name = f"Monitor {random.choice(BRANDS)} 24 pulgadas"
            related_categories = ["Gaming"]

        elif category_name == "Redes":
            name = f"Router {random.choice(BRANDS)} Dual Band"
            related_categories = ["Gaming"]

        elif category_name == "Gaming":
            name = f"Gaming {random.choice(['Laptop', 'Mouse', 'Teclado'])} RGB"
            related_categories = ["Laptops", "Accesorios"]

        else:
            name = "Producto Genérico"
            related_categories = []

        # Elegimos segunda categoría coherente
        possible_second = [
            category_dict[cat]
            for cat in related_categories
            if cat in category_dict
        ]

        if possible_second:
            category_id_2 = random.choice(possible_second)
            category_ids = [category_id_1, category_id_2]
        else:
            category_ids = [category_id_1]

        data = {
            "name": name + f"_{success}_{random.randint(1000,9999)}",
            "price": round(random.uniform(50, 3000), 2),
            "description": f"{category_name} de alta calidad",
            "userId": random.choice(user_ids),
            "categoryIds": category_ids
        }

        r = requests.post(API_PRODUCTS, json=data)

        if r.status_code in [200, 201]:
            success += 1

            if success % 100 == 0:
                print(f"{success} productos creados...")
        else:
            print("Error producto:", r.status_code, r.text)

        time.sleep(0.02)

    print("\n1000 productos creados correctamente.")


# =============================
# MAIN
# =============================
if __name__ == "__main__":

    print("=================================")
    print(" GENERADOR MASIVO DE DATOS")
    print("=================================")

    users = create_users()
    categories = create_categories()

    if users and categories:
        create_products(users, categories)
    else:
        print("Error: No se pudieron crear usuarios o categorías.")