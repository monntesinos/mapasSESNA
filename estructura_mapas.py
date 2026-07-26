import mapas

def main():
    print("=== ¿Qué información quieres consultar? ===")
    print("1. Estatal")
    print("2. Municipal")
    opcion = input("Elige una opción (1 o 2): ").strip()

    if opcion == "1":
        mapa = mapas.generar_mapa_estatal()
        mapa.save("mapa_resultado.html")
        print("¡Listo! Mapa estatal guardado en 'mapa_resultado.html'.")

    elif opcion == "2":
        estados_disponibles = mapas.listar_estados_disponibles()

        print("\n=== Estados disponibles ===")
        for i, estado in enumerate(estados_disponibles, start=1):
            print(f"{i}. {estado}")

        seleccion = input("\nElige el número del estado: ").strip()

        try:
            indice = int(seleccion) - 1
            estado_elegido = estados_disponibles[indice]
        except (ValueError, IndexError):
            print("Opción inválida.")
            return

        mapa = mapas.generar_mapa_municipal(estado_elegido)
        mapa.save("mapa_resultado.html")
        print(f"¡Listo! Mapa municipal de '{estado_elegido}' guardado en 'mapa_resultado.html'.")

    else:
        print("Opción inválida, elige 1 o 2.")


if __name__ == "__main__":
    main()