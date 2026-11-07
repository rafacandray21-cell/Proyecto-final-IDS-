# Programa de inventario de la distribuidora de Emilio
# Introducción al Desarrollo de Software

# ----- Datos iniciales -----
# Artículo y marcas que maneja cada código
Inventarios = {
    "LP01": {
        "articulo": "Laptop",
        "marcas": [
            "MacBook",
            "HP",
            "Dell"
        ]
    },
    "MS01": {
        "articulo": "Mouse",
        "marcas": [
            "Logitech",
            "Razer",
            "HP"
        ]
    },
    "TC01": {
        "articulo": "Teclado",
        "marcas": [
            "Logitech",
            "Redragon",
            "Corsair"
        ]
    },
    "AU01": {
        "articulo": "Audifonos",
        "marcas": [
            "Sony",
            "JBL",
            "Apple"
        ]
    },
    "CE01": {
        "articulo": "Celular",
        "marcas": [
            "Samsung",
            "iPhone",
            "Xiaomi"
        ]
    }
}

# Unidades disponibles de cada marca dentro de cada código
existencias = {
    "LP01": {"MacBook": 10, "HP": 15, "Dell": 20},
    "MS01": {"Logitech": 40, "Razer": 25, "HP": 30},
    "TC01": {"Logitech": 30, "Redragon": 20, "Corsair": 12},
    "AU01": {"Sony": 35, "JBL": 40, "Apple": 18},
    "CE01": {"Samsung": 22, "iPhone": 14, "Xiaomi": 28},
}

# Tiendas minoristas que compran a Emilio
tiendas = {
    "1": "Radioshack",
    "2": "Curacao",
    "3": "Siman",
    "4": "Ishop",
}

MINIMO_EXISTENCIAS = 5


# ----- Funciones de apoyo -----
def pedir_entero(mensaje):
    # Repite la pregunta hasta que se escriba un número entero mayor a cero
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Dato inválido. Escriba un número entero mayor a cero.")


def mostrar_codigos():
    print("\nCódigos disponibles:")
    for codigo in Inventarios:
        print(codigo, "-", Inventarios[codigo]["articulo"])


def elegir_marca(codigo, permitir_nueva):
    # Muestra las marcas del código con un número y devuelve la marca elegida
    marcas = Inventarios[codigo]["marcas"]
    print("\nMarcas de", Inventarios[codigo]["articulo"] + ":")
    numero = 1
    for marca in marcas:
        print(str(numero) + ".", marca)
        numero = numero + 1
    if permitir_nueva:
        print(str(numero) + ".", "Agregar marca nueva")

    opcion = input("Marca (número): ").strip()
    if not opcion.isdigit():
        print("Opción inválida.")
        return ""
    opcion = int(opcion)

    if opcion >= 1 and opcion <= len(marcas):
        return marcas[opcion - 1]

    if permitir_nueva and opcion == len(marcas) + 1:
        nueva = input("Nombre de la marca nueva: ").strip()
        if nueva == "":
            print("Dato inválido. El nombre no puede estar vacío.")
            return ""
        if nueva in marcas:
            print("Esa marca ya existe.")
            return nueva
        marcas.append(nueva)
        existencias[codigo][nueva] = 0
        return nueva

    print("Opción inválida. Esa marca no está en la lista.")
    return ""


def avisar_si_bajo(codigo, marca):
    if existencias[codigo][marca] <= MINIMO_EXISTENCIAS:
        print("ALERTA: quedan", existencias[codigo][marca], "unidades de",
              Inventarios[codigo]["articulo"], marca)


# ----- Opción 1 -----
def consultar_existencias():
    print("\n---Tienda de Emilio---")
    for codigo in Inventarios:
        articulo = Inventarios[codigo]["articulo"]
        print("\n" + articulo, "(" + codigo + ")")
        for marca in Inventarios[codigo]["marcas"]:
            print("  Existencia de", articulo, marca + ":", existencias[codigo][marca])
            avisar_si_bajo(codigo, marca)


# ----- Opción 2 -----
def ingresar_entrada():
    mostrar_codigos()
    codigo = input("Inventario que se abastece (código del producto): ").strip().upper()
    if codigo == "":
        print("Dato inválido. El código no puede estar vacío.")
        return

    if codigo not in Inventarios:
        print("El código", codigo, "no existe. Se registrará como artículo nuevo.")
        articulo = input("Nombre del artículo nuevo: ").strip()
        marca = input("Marca del artículo nuevo: ").strip()
        if articulo == "" or marca == "":
            print("Dato inválido. Los nombres no pueden estar vacíos. No se hicieron cambios.")
            return
        Inventarios[codigo] = {"articulo": articulo, "marcas": [marca]}
        existencias[codigo] = {marca: 0}
    else:
        marca = elegir_marca(codigo, True)
        if marca == "":
            return

    cantidad = pedir_entero("Cantidad de producto: ")
    existencias[codigo][marca] = existencias[codigo][marca] + cantidad
    print("Entrada registrada.", Inventarios[codigo]["articulo"], marca,
          "ahora tiene", existencias[codigo][marca], "unidades.")


# ----- Opción 3 -----
def elegir_tienda():
    print("\nTiendas registradas:")
    for numero in tiendas:
        print(numero + ".", tiendas[numero])
    numero = input("Tienda que retira el producto (número): ").strip()
    if numero in tiendas:
        return tiendas[numero]
    print("Opción inválida. Esa tienda no está en la lista.")
    return ""


def ingresar_salida():
    tienda = elegir_tienda()
    if tienda == "":
        return

    # La orden guarda código -> {marca: cantidad}; el inventario no cambia hasta confirmar
    orden = {}
    print("\nAgregue los productos de la orden. Escriba 0 en el código para terminar.")
    while True:
        mostrar_codigos()
        codigo = input("Inventario que se retira (código del producto): ").strip().upper()
        if codigo == "0":
            break
        if codigo not in Inventarios:
            print("El código", codigo, "no existe en el inventario.")
            continue

        marca = elegir_marca(codigo, False)
        if marca == "":
            continue

        cantidad = pedir_entero("Cantidad de producto: ")
        if codigo not in orden:
            orden[codigo] = {}
        ya_pedido = orden[codigo].get(marca, 0)
        disponible = existencias[codigo][marca] - ya_pedido
        if cantidad > disponible:
            print("No hay suficientes existencias. Solo quedan", disponible, "unidades de",
                  Inventarios[codigo]["articulo"], marca)
            if len(orden[codigo]) == 0:
                del orden[codigo]
            continue

        orden[codigo][marca] = ya_pedido + cantidad
        print("Agregado:", cantidad, "x", Inventarios[codigo]["articulo"], marca)

    if len(orden) == 0:
        print("La orden está vacía. No se hicieron cambios.")
        return

    print("\nResumen de la orden para", tienda)
    for codigo in orden:
        for marca in orden[codigo]:
            print("-", orden[codigo][marca], "x", Inventarios[codigo]["articulo"], marca)

    confirmar = input("¿Confirmar la orden? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Orden cancelada. No se hicieron cambios.")
        return

    for codigo in orden:
        for marca in orden[codigo]:
            existencias[codigo][marca] = existencias[codigo][marca] - orden[codigo][marca]
            avisar_si_bajo(codigo, marca)
    print("Salida registrada para", tienda)


# ----- Menú principal -----
def menu():
    while True:
        print("\nBienvenido al menú de la tienda de Emilio, por favor seleccione una opción")
        print("1. Consultar existencias")
        print("2. Ingresar entrada de inventario")
        print("3. Ingresar salida de inventario")
        print("4. Cerrar el menú")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            consultar_existencias()
        elif opcion == "2":
            ingresar_entrada()
        elif opcion == "3":
            ingresar_salida()
        elif opcion == "4":
            print("\n--Buen día--")
            break
        else:
            print("Opción inválida. Escriba un número del 1 al 4.")


menu()