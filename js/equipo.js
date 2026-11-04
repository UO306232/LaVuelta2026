class Equipo {
    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;

        this.director = null;
        this.categoria = null;
        this.paginaWeb = null;
    }

    rellenarAtributos(director, categoria, paginaWeb) {
        this.director = director;
        this.categoria = categoria;
        this.paginaWeb = paginaWeb;
    }

    datosBasicos() {
        return this.nombre + " (" + this.codigoUCI + ")";
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        let html = "<ul>";
        html += "<li>Director: " + this.director + "</li>";
        html += "<li>Categoría: " + this.categoria + "</li>";
        html += "</ul>";
        return html;
    }

    getPaginaWeb() {
        const primeraSeccion = document.querySelector("main section");

        if (primeraSeccion) {
            const parrafo = document.createElement("p");
            const enlace = document.createElement("a");

            enlace.href = this.paginaWeb;
            enlace.textContent = "Ficha oficial del equipo en La Vuelta";
            enlace.target = "_blank";

            parrafo.appendChild(enlace);
            primeraSeccion.appendChild(parrafo);
        } else {
            console.error("No se encontró ninguna etiqueta <section> en el documento HTML");
        }
    }
}

const miEquipo = new Equipo("Bahrain Victorious", "TBV", "Baréin");
miEquipo.rellenarAtributos("Pellizotti franco", "UCI WorldTeam", "https://www.lavuelta.es/es/equipo/TBV/bahrain-victorius");

const nuevaSeccionEquipo = document.createElement("section");

const tituloH3Equipo = document.createElement("h3");
tituloH3Equipo.textContent = miEquipo.datosBasicos() + " - " + miEquipo.getPais();
nuevaSeccionEquipo.appendChild(tituloH3Equipo);

nuevaSeccionEquipo.insertAdjacentHTML("beforeend", miEquipo.getInformacionSecundaria());

const encabezadoH2Equipo = document.querySelector("main h2");
if (encabezadoH2Equipo) {
    encabezadoH2Equipo.insertAdjacentElement("afterend", nuevaSeccionEquipo);
}

miEquipo.getPaginaWeb();