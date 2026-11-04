class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;

        this.poblacion = null;
        this.coordenadas = {
            latitud: null,
            longitud: null,
            altitud: null
        };
    }

    rellenarAtributos(poblacion, latitud, longitud, altitud) {
        this.poblacion = poblacion;
        this.coordenadas.latitud = latitud;
        this.coordenadas.longitud = longitud;
        this.coordenadas.altitud = altitud;
    }

    getCiudad() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        let html = "<ul>";
        html += "<li>Gentilicio: " + this.gentilicio + "</li>";
        html += "<li>Población: " + this.poblacion.toLocaleString() + " habitantes</li>";
        html += "</ul>";
        return html;
    }

    escribeCoordenadas() {
        const primeraSeccion = document.querySelector("main section");

        if (primeraSeccion) {
            const parrafo = document.createElement("p");
            parrafo.textContent = "Coordenadas del punto central: Latitud " + this.coordenadas.latitud +
            "º, Longitud " + this.coordenadas.longitud + 
            "º, Altitud " + this.coordenadas.altitud + " metros.";

            primeraSeccion.appendChild(parrafo);
        } else {
            console.error("No se encontró ninguna etiqueta <section> en el documento HTML");
        }
    }
}

const miCiudad = new Ciudad("Cartagena", "España", "Cartagenero/a");
miCiudad.rellenarAtributos(222559, 37.6051, -0.9862, 67);

const nuevaSeccion = document.createElement("section");

const tituloH3 = document.createElement("h3");
tituloH3.textContent = miCiudad.getCiudad() + " (" + miCiudad.getPais() + ")";
nuevaSeccion.appendChild(tituloH3);

nuevaSeccion.insertAdjacentHTML("beforeend", miCiudad.getInformacionSecundaria());

const encabezadoH2 = document.querySelector("main h2");
if (encabezadoH2) {
    encabezadoH2.insertAdjacentElement("afterend", nuevaSeccion);
}

miCiudad.escribeCoordenadas();