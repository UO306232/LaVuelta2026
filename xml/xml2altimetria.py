import xml.etree.ElementTree as ET

class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    Basado estrictamente en el ejemplo 02030-SVG.py del profesor.
    """
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0",
                               width="1200", height="600")

    def addRect(self, x, y, width, height, fill, strokeWidth, stroke):
        ET.SubElement(self.raiz, 'rect', x=x, y=y, width=width, height=height,
                      fill=fill, stroke=stroke, **{'stroke-width': strokeWidth})
        
    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth):
        ET.SubElement(self.raiz, 'line', x1=x1, y1=y1, x2=x2, y2=y2,
                      stroke=stroke, **{'stroke-width': strokeWidth})

    def addPolyline(self, points, stroke, strokeWidth, fill):
        ET.SubElement(self.raiz, 'polyline', points=points, stroke=stroke,
                      fill=fill, **{'stroke-width': strokeWidth})
        
    def addText(self, texto, x, y, fontFamily, fontSize, style):
        ET.SubElement(self.raiz, 'text', x=x, y=y, fontFamily=fontFamily,
                      fontSize=fontSize, style=style).text = texto

    def escribir(self, nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)


class ProcesadorAltimetria(object):
    def __init__(self, archivo_xml):
        self.archivo_xml = archivo_xml
        self.ns = {'uniovi': 'http://www.uniovi.es'}
        self.svg = Svg()

    def procesar(self, archivo_salida_svg):
        tree = ET.parse(self.archivo_xml)
        raiz = tree.getroot()

        datos_perfil = []
        
        # Longitud y desnivel
        nodo_longitud = raiz.find('.//uniovi:longitudEtapa', self.ns)
        distancia_total = float(nodo_longitud.attrib['distance']) if nodo_longitud is not None else 153.8
        
        nodo_desnivel = raiz.find('.//uniovi:desnivelEtapa', self.ns)
        desnivel_total = nodo_desnivel.attrib['height'] if nodo_desnivel is not None else "1351"

        # Extraer puntos
        salida = raiz.find('.//uniovi:lugarSalida', self.ns)
        if salida is not None:
            datos_perfil.append({'dist': 0.0, 'alt': float(salida.attrib['altitud']), 'nombre': salida.text.strip(), 'relevante': True})

        for p in raiz.findall('.//uniovi:puntosAnonimos/uniovi:punto', self.ns):
            datos_perfil.append({'dist': float(p.attrib['distance']), 'alt': float(p.attrib['altitud']), 'nombre': '', 'relevante': False})

        for h in raiz.findall('.//uniovi:hitos/uniovi:hito', self.ns):
            datos_perfil.append({'dist': float(h.attrib['distance']), 'alt': float(h.attrib['altitud']), 'nombre': h.text.strip(), 'relevante': True})

        meta = raiz.find('.//uniovi:lugarMeta', self.ns)
        if meta is not None:
            datos_perfil.append({'dist': distancia_total, 'alt': float(meta.attrib['altitud']), 'nombre': meta.text.strip(), 'relevante': True})

        datos_perfil.sort(key=lambda item: item['dist'])

        # --- PARÁMETROS DE DIBUJO ---
        margen_izq = 120
        margen_inf = 450
        ancho_dibujo = 950
        alto_dibujo = 250
        altitud_maxima = 800  
        x_final = margen_izq + ancho_dibujo

        # Fondo blanco
        self.svg.addRect('0', '0', '1200', '600', 'white', '0', 'none')

        # 1. Dibujar marcas, textos del eje Y con "m" y líneas guía horizontales
        for alt_y in range(0, 801, 200):
            y_px = margen_inf - (alt_y / altitud_maxima) * alto_dibujo
            
            # Línea horizontal guía (gris claro) cruzando la gráfica
            self.svg.addLine(str(margen_izq), str(y_px), str(x_final), str(y_px), '#cccccc', '1')
            
            # Pequeña marca negra en el eje
            self.svg.addLine(str(margen_izq - 5), str(y_px), str(margen_izq), str(y_px), 'black', '1')
            
            # Texto alineado a la derecha con "m" (ej. "200 m")
            self.svg.addText(f"{alt_y} m", str(margen_izq - 10), str(y_px + 4), "Verdana", "10", "text-anchor: end;")

        # 2. Construir la polilínea del terreno
        puntos_str = f"{margen_izq},{margen_inf} "
        for p in datos_perfil:
            x = margen_izq + (p['dist'] / distancia_total) * ancho_dibujo
            y = margen_inf - (p['alt'] / altitud_maxima) * alto_dibujo
            puntos_str += f"{x:.1f},{y:.1f} "
        
        puntos_str += f"{x_final},{margen_inf}"

        # Relleno rojo oficial
        self.svg.addPolyline(puntos_str.strip(), '#c02010', '1', '#e83820')

        # Eje X base (línea negra de suelo)
        self.svg.addLine(str(margen_izq), str(margen_inf), str(x_final), str(margen_inf), 'black', '2')

        # 3. Dibujar hitos (Líneas verticales y textos)
        estilo_vertical = "writing-mode: tb; glyph-orientation-vertical: 0;"
        
        for p in datos_perfil:
            if p['relevante']:
                x = margen_izq + (p['dist'] / distancia_total) * ancho_dibujo
                y_terreno = margen_inf - (p['alt'] / altitud_maxima) * alto_dibujo
                
                # Línea vertical desde el terreno hasta la zona de etiquetas
                self.svg.addLine(str(x), "80", str(x), str(y_terreno), 'gray', '1')
                
                # Rótulo de texto: "Nombre / Altitud m" desplazado a la derecha
                etiqueta = f"{p['nombre']} / {int(p['alt'])} m"
                self.svg.addText(etiqueta, str(x + 8), "20", "Verdana", "12", estilo_vertical)

                # Rótulo de distancia en el eje X inferior SIEMPRE con "km"
                texto_dist = f"{str(p['dist']).replace('.', ',')} km"
                self.svg.addText(texto_dist, str(x), str(margen_inf + 20), "Verdana", "11", "text-anchor: middle;")

        # 4. Título inferior centrado
        texto_desnivel = f"Desnivel positivo: {desnivel_total} m"
        centro_x = margen_izq + (ancho_dibujo / 2)
        self.svg.addText(texto_desnivel, str(centro_x), str(margen_inf + 70), "Verdana", "18", "font-weight: bold; text-anchor: middle;")

        self.svg.escribir(archivo_salida_svg)
        print(f"Archivo SVG '{archivo_salida_svg}' generado con éxito.")


class Aplicacion(object):
    def ejecutar(self):
        generador = ProcesadorAltimetria("etapaEsquema.xml")
        generador.procesar("altimetria.svg")

if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()