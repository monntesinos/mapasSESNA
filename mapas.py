import folium
import json

# --- CARGA DE DATOS (una sola vez, al importar el módulo) ---
print("Cargando datos geográficos desde disco...")

with open("data/estados.json", "r", encoding="utf-8") as f:
    DATOS_ESTADOS = json.load(f)

with open("data/municipios.json", "r", encoding="utf-8") as f:
    DATOS_MUNICIPIOS = json.load(f)

print("¡Datos cargados con éxito!")


# --- FUNCIÓN 1: MAPA ESTATAL ---
def generar_mapa_estatal():
    print("Creando mapa estatal...")
    mapa = folium.Map(location=[23.6345, -102.5528], zoom_start=5)

    folium.GeoJson(
        DATOS_ESTADOS,
        name="Estados de México",
        style_function=lambda feature: {
            'fillColor': '#3186cc',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.4
        }
    ).add_to(mapa)

    return mapa


# --- FUNCIÓN 2: MAPA MUNICIPAL ---
def generar_mapa_municipal(estado_seleccionado=None):
    print(f"Preparando mapa municipal para: {estado_seleccionado}")

    # 1. Preparamos el molde vacío
    datos_filtrados = {
        "type": "FeatureCollection",
        "features": []
    }

    # 2. EL FILTRO (con validación de geometría incluida)
    if estado_seleccionado is not None:
        for municipio in DATOS_MUNICIPIOS["features"]:
            estado_del_municipio = municipio["properties"].get("NAME_1")
            geometria = municipio.get("geometry")

            if (estado_del_municipio
                and estado_seleccionado.lower() in estado_del_municipio.lower()
                and geometria is not None
                and geometria.get("coordinates")):
                datos_filtrados["features"].append(municipio)
    else:
        datos_filtrados = DATOS_MUNICIPIOS

    # 3. EL SEGURO
    mapa = folium.Map(location=[23.6345, -102.5528], zoom_start=5)
    cantidad = len(datos_filtrados["features"])

    if cantidad == 0:
        print(f"ALERTA GIGANTE: La lista quedó vacía. El estado '{estado_seleccionado}' no se encontró en el archivo.")
        return mapa

    print(f"¡Éxito! Encontramos {cantidad} municipios. Dibujando y moviendo la cámara...")

    # 4. DIBUJAR Y ENCUADRAR
    capa_municipios = folium.GeoJson(
        datos_filtrados,
        name=f"Municipios de {estado_seleccionado}",
        style_function=lambda feature: {
            'fillColor': '#ff851b',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.4
        }
    )

    capa_municipios.add_to(mapa)

    if estado_seleccionado is not None:
        mapa.fit_bounds(capa_municipios.get_bounds())

    return mapa


# --- FUNCIÓN 3: LISTAR ESTADOS DISPONIBLES ---
def listar_estados_disponibles():
    estados = set()
    for municipio in DATOS_MUNICIPIOS["features"]:
        nombre_estado = municipio["properties"].get("NAME_1")
        if nombre_estado:
            estados.add(nombre_estado)
    return sorted(estados)

# --- ZONA DE PRUEBAS ---
if __name__ == "__main__":

    mapa_estatal = generar_mapa_estatal()
    mapa_estatal.save("prueba_estatal.html")
    print("¡Listo! Archivo 'prueba_estatal.html' guardado.\n")

    mapa_muni = generar_mapa_municipal("Sonora")
    mapa_muni.save("prueba_municipal.html")
    print("¡Listo! Archivo 'prueba_municipal.html' guardado.")