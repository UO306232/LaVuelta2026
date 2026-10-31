import xml.etree.ElementTree as ET

class Kml(object):
    """
    Genera archivo KML con puntos y líneas
    """
    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz,'Document')

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud, color):
        """
        Añade un elemento <Placemark> con puntos <Point> y color básico
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        
        # Estilo de color básico
        estilo = ET.SubElement(pm, 'Style')
        icono = ET.SubElement(estilo, 'IconStyle')
        ET.SubElement(icono, 'color').text = color
        
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long, lat, alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement (linea, 'color').text = color
        ET.SubElement (linea, 'width').text = ancho

    def escribir(self, nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)


class ProcesadorEtapaKml(object):
    """
    Lee el archivo XML mediante XPath y usa la clase Kml (POO)
    """
    def __init__(self, archivo_xml):
        self.archivo_xml = archivo_xml
        self.ns = {'uniovi': 'http://www.uniovi.es'}
        self.kml = Kml()

    def procesar(self, archivo_salida_kml):
        tree = ET.parse(self.archivo_xml)
        raiz = tree.getroot()

        coordenadas_linea = []
        coords_hitos = set() # Para no duplicar puntos anónimos donde ya hay hitos

        # 1. Salida (Rojo: ff0000ff)
        salida = raiz.find('.//uniovi:lugarSalida', self.ns)
        if salida is not None:
            lon = salida.attrib['longitud']
            lat = salida.attrib['latitud']
            alt = salida.attrib['altitud']
            self.kml.addPlacemark("Salida: " + salida.text.strip(), "Inicio", lon, lat, alt, 'relativeToGround', 'ff0000ff')
            coordenadas_linea.append(f"{lon},{lat},{alt}")

        # 2. Hitos (Puertos Verde: ff00ff00 | Sprints Azul: ffff0000)
        hitos = raiz.findall('.//uniovi:hitos/uniovi:hito', self.ns)
        for h in hitos:
            lon = h.attrib['longitud']
            lat = h.attrib['latitud']
            alt = h.attrib['altitud']
            texto = h.text.strip()
            coords_hitos.add((lon, lat))
            
            color = 'ff00ff00' if "Puerto" in texto or "Alto" in texto else 'ffff0000'
            self.kml.addPlacemark(texto, "Hito", lon, lat, alt, 'relativeToGround', color)

        # 3. Puntos Anónimos (Amarillo: ff00ffff)
        puntos = raiz.findall('.//uniovi:puntosAnonimos/uniovi:punto', self.ns)
        for p in puntos:
            lon = p.attrib['longitud']
            lat = p.attrib['latitud']
            alt = p.attrib['altitud']
            coordenadas_linea.append(f"{lon},{lat},{alt}")
            
            if (lon, lat) not in coords_hitos:
                self.kml.addPlacemark("Punto", "Intermedio", lon, lat, alt, 'relativeToGround', 'ff00ffff')

        # 4. Meta (Rojo: ff0000ff)
        meta = raiz.find('.//uniovi:lugarMeta', self.ns)
        if meta is not None:
            lon = meta.attrib['longitud']
            lat = meta.attrib['latitud']
            alt = meta.attrib['altitud']
            self.kml.addPlacemark("Meta: " + meta.text.strip(), "Fin", lon, lat, alt, 'relativeToGround', 'ff0000ff')
            coordenadas_linea.append(f"{lon},{lat},{alt}")

        # 5. Trazar la Línea
        cadena_coordenadas = "\n".join(coordenadas_linea)
        nombre_etapa = raiz.find('.//uniovi:name', self.ns)
        titulo = nombre_etapa.text.strip() if nombre_etapa is not None else "Recorrido"

        self.kml.addLineString(
            f"Ruta - {titulo}",
            "1", "1",
            cadena_coordenadas,
            'relativeToGround',
            '#ff0000ff', "5"
        )

        self.kml.escribir(archivo_salida_kml)


class Aplicacion(object):
    def ejecutar(self):
        procesador = ProcesadorEtapaKml("etapaEsquema.xml")
        procesador.procesar("etapa.kml")


if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()