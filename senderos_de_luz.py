#!/usr/bin/env python3
"""Senderos de Luz - Juego narrativo cooperativo inspirado en la Biblia.

El juego busca motivar a jugadores de cualquier edad a leer y reflexionar
sobre la Biblia mediante rutas temáticas, preguntas interactivas y premios
que desbloquean obstáculos llamados Puertas de Sabiduría.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from textwrap import fill

# Constantes de modo para personalizar la narrativa según preferencia.
MODO_CUENTO = "cuento"
MODO_ESTRATEGIA = "estrategia"
MODO_REFLEXION = "reflexion"

# Virtudes disponibles como cartas de apoyo.
VIRTUDES_BASE = {
    "Paciencia": 1,
    "Discernimiento": 1,
    "Servicio": 1,
}


def envolver(texto: str) -> str:
    """Devuelve el texto formateado en párrafos legibles para la consola."""
    return "\n".join(fill(line.strip(), width=78) if line.strip() else ""
                     for line in texto.splitlines())


@dataclass
class Recompensa:
    gemas: int = 0
    virtud: str | None = None
    recuerdo: str | None = None


@dataclass
class Capitulo:
    titulo: str
    narrativa: dict[str, str]
    pregunta: str
    opciones: list[str]
    respuesta: str
    pista: str
    explicacion: str
    obstaculo: str
    reflexion: str
    recompensa: Recompensa


@dataclass
class Camino:
    nombre: str
    descripcion: str
    capitulos: list[Capitulo]


@dataclass
class Jugador:
    nombre: str
    grupo_edad: str
    modo: str
    gemas: int = 0
    virtudes: dict[str, int] = field(default_factory=lambda: VIRTUDES_BASE.copy())
    testimonios: list[dict[str, str]] = field(default_factory=list)

    def ganar_gemas(self, cantidad: int) -> None:
        self.gemas += cantidad

    def ganar_virtud(self, virtud: str) -> None:
        self.virtudes[virtud] = self.virtudes.get(virtud, 0) + 1

    def usar_virtud(self, virtud: str) -> bool:
        disponible = self.virtudes.get(virtud, 0)
        if disponible > 0:
            self.virtudes[virtud] = disponible - 1
            return True
        return False

    def registrar_testimonio(self, camino: str, capitulo: str, texto: str) -> None:
        self.testimonios.append({
            "camino": camino,
            "capitulo": capitulo,
            "texto": texto.strip(),
        })


def crear_camino_patriarcas() -> Camino:
    capitulos = [
        Capitulo(
            titulo="El llamado de Abram",
            narrativa={
                MODO_CUENTO: (
                    "Dios invitó a Abram a caminar hacia una tierra nueva. "
                    "Aunque no sabía qué encontraría, confió y dio el primer paso."
                ),
                MODO_ESTRATEGIA: (
                    "Abram respondió a la promesa de Dios dejando su tierra y "
                    "familia. El viaje inició con un acto radical de confianza."
                ),
                MODO_REFLEXION: (
                    "El llamado a Abram abre la puerta a una historia de fe "
                    "que se sostiene en la promesa divina. Contemplar su "
                    "desapego invita a pensar en nuestros propios desarraigos."
                ),
            },
            pregunta="¿Qué representaba para Abram dejar su hogar según Génesis 12?",
            opciones=[
                "A) Una competencia con su familia.",
                "B) Un sacrificio al que fue obligado.",
                "C) Un acto de confianza en la promesa de Dios.",
                "D) Un viaje turístico por curiosidad.",
            ],
            respuesta="C",
            pista="Piensa en la relación entre promesa y confianza.",
            explicacion=(
                "Abram obedeció en confianza porque Dios le prometió bendecirlo "
                "y hacerlo una gran nación."
            ),
            obstaculo="Puerta de Sabiduría: ¿Te atreves a confiar en una promesa?",
            reflexion="¿Qué promesa recuerdas hoy que te anima a avanzar?",
            recompensa=Recompensa(gemas=3, virtud="Discernimiento",
                                  recuerdo="Ilustración del viaje de Abram"),
        ),
        Capitulo(
            titulo="El sueño de Jacob",
            narrativa={
                MODO_CUENTO: (
                    "Jacob durmió con una piedra por almohada y soñó con una "
                    "escalera por donde subían y bajaban ángeles."
                ),
                MODO_ESTRATEGIA: (
                    "En Betel, Jacob percibió la presencia de Dios mediante un "
                    "sueño que confirmó el pacto con sus padres."
                ),
                MODO_REFLEXION: (
                    "El encuentro de Jacob en Betel recuerda que la fidelidad "
                    "divina alcanza generaciones. La escalera simboliza la "
                    "unión entre lo humano y lo celestial."
                ),
            },
            pregunta="¿Qué hizo Jacob al despertar de su sueño en Betel?",
            opciones=[
                "A) Construyó un altar y prometió seguir a Dios.",
                "B) Se fue sin decir nada a nadie.",
                "C) Llamó a Esaú para pedirle ayuda.",
                "D) Decidió abandonar su fe.",
            ],
            respuesta="A",
            pista="Observa cómo respondió Jacob ante lo sagrado.",
            explicacion=(
                "Jacob reconoció a Betel como 'casa de Dios' y erigió una "
                "columna, comprometiéndose a seguir al Señor."
            ),
            obstaculo="Puerta de Sabiduría: Reconocer la presencia de Dios.",
            reflexion="Describe un lugar que se haya vuelto significativo para tu fe.",
            recompensa=Recompensa(gemas=4, virtud="Paciencia",
                                  recuerdo="Audio de Jacob bendiciendo a sus hijos"),
        ),
    ]
    return Camino(
        nombre="Patriarcas",
        descripcion="Inicia el recorrido con las primeras promesas y rutas de fe.",
        capitulos=capitulos,
    )


def crear_camino_profetas() -> Camino:
    capitulos = [
        Capitulo(
            titulo="Isaías anuncia consuelo",
            narrativa={
                MODO_CUENTO: (
                    "El profeta Isaías habló al pueblo triste y le recordó que "
                    "Dios no los había olvidado."
                ),
                MODO_ESTRATEGIA: (
                    "Isaías 40 ofrece palabras de consuelo para un pueblo en "
                    "exilio, apuntando a la fidelidad de Dios."
                ),
                MODO_REFLEXION: (
                    "El 'Consuélense, consuélense' de Isaías abre una liturgia "
                    "de esperanza en medio del desarraigo."
                ),
            },
            pregunta="¿Qué imagen usa Isaías 40 para describir el cuidado de Dios?",
            opciones=[
                "A) Un rey distante.",
                "B) Un pastor que carga a sus ovejas.",
                "C) Un soldado en batalla.",
                "D) Un comerciante justo.",
            ],
            respuesta="B",
            pista="Busca una figura tierna y cercana.",
            explicacion=(
                "Isaías describe a Dios como un pastor que alimenta, reúne y "
                "lleva en brazos a los corderos."
            ),
            obstaculo="Puerta de Sabiduría: Recibir consuelo y compartirlo.",
            reflexion="¿A quién podrías consolar hoy con palabras de esperanza?",
            recompensa=Recompensa(gemas=3, virtud=None,
                                  recuerdo="Mini video: Voz de esperanza en el exilio"),
        ),
        Capitulo(
            titulo="Miqueas y la justicia",
            narrativa={
                MODO_CUENTO: (
                    "Miqueas le dijo al pueblo que ser amigo de Dios es hacer "
                    "lo correcto, amar y vivir con humildad."
                ),
                MODO_ESTRATEGIA: (
                    "Miqueas 6:8 resume la ética profética: justicia, amor "
                    "misericordioso y humildad ante Dios."
                ),
                MODO_REFLEXION: (
                    "La síntesis de Miqueas confronta las falsas seguridades "
                    "religiosas y exige una espiritualidad comprometida con la "
                    "justicia."
                ),
            },
            pregunta="Según Miqueas 6:8, ¿qué pide Dios al pueblo?",
            opciones=[
                "A) Sacrificios costosos.",
                "B) Conquistar nuevas tierras.",
                "C) Practicar la justicia, amar la misericordia y ser humilde.",
                "D) Guardar silencio absoluto.",
            ],
            respuesta="C",
            pista="Es una tríada que equilibra acción y corazón.",
            explicacion=(
                "El texto invita a una vida que combine justicia, misericordia "
                "y humildad frente a Dios."
            ),
            obstaculo="Puerta de Sabiduría: La justicia comienza en pequeñas acciones.",
            reflexion="Escribe un gesto concreto de justicia que quieras realizar.",
            recompensa=Recompensa(gemas=4, virtud="Servicio",
                                  recuerdo="Ilustración colaborativa: Caminos de justicia"),
        ),
    ]
    return Camino(
        nombre="Profetas",
        descripcion="Voces que animan, corrigen y sostienen la esperanza del pueblo.",
        capitulos=capitulos,
    )


def crear_camino_evangelios() -> Camino:
    capitulos = [
        Capitulo(
            titulo="El llamado de los discípulos",
            narrativa={
                MODO_CUENTO: (
                    "Jesús invitó a pescadores sencillos a seguirlo. Dejaron "
                    "sus redes y se unieron a su misión."
                ),
                MODO_ESTRATEGIA: (
                    "En los Evangelios, Jesús convoca a los primeros discípulos "
                    "para enseñarles a pescar personas y formar comunidad."
                ),
                MODO_REFLEXION: (
                    "El seguimiento discipular requiere disponibilidad. "
                    "Contemplemos qué redes necesitamos soltar hoy."
                ),
            },
            pregunta="¿Qué hicieron Simón y Andrés cuando Jesús los llamó?",
            opciones=[
                "A) Ignoraron a Jesús.",
                "B) Le pidieron más tiempo.",
                "C) Dejaron las redes y lo siguieron.",
                "D) Vendieron sus barcas y se fueron a otra ciudad.",
            ],
            respuesta="C",
            pista="Piensa en la inmediatez de su respuesta.",
            explicacion=(
                "Los discípulos respondieron con prontitud, dejando las redes "
                "para seguir a Jesús."
            ),
            obstaculo="Puerta de Sabiduría: Soltar redes para abrazar una misión nueva.",
            reflexion="Menciona una invitación de Jesús que te desafíe hoy.",
            recompensa=Recompensa(gemas=3, virtud=None,
                                  recuerdo="Audio: Voces junto al mar de Galilea"),
        ),
        Capitulo(
            titulo="La multiplicación de los panes",
            narrativa={
                MODO_CUENTO: (
                    "Un niño compartió sus panes y peces. Jesús los bendijo y "
                    "alcanzaron para toda la multitud."
                ),
                MODO_ESTRATEGIA: (
                    "Con cinco panes y dos peces, la multitud fue alimentada, "
                    "mostrando la generosidad que brota de compartir."
                ),
                MODO_REFLEXION: (
                    "La multiplicación revela la economía del Reino: lo poco "
                    "puede transformarse en abundancia cuando se comparte."
                ),
            },
            pregunta="¿Qué detalle resalta el milagro de los panes?",
            opciones=[
                "A) Jesús guardó los panes para otro día.",
                "B) La abundancia vino de compartir un recurso pequeño.",
                "C) Nadie quiso comer.",
                "D) Los discípulos no participaron.",
            ],
            respuesta="B",
            pista="Observa cómo participa la comunidad en el milagro.",
            explicacion=(
                "El gesto de compartir lo poco disponible abrió la puerta a la "
                "abundancia para todos."
            ),
            obstaculo="Puerta de Sabiduría: Compartir para multiplicar.",
            reflexion="Anota algo concreto que podrías compartir esta semana.",
            recompensa=Recompensa(gemas=5, virtud="Servicio",
                                  recuerdo="Cofre multimedia: Canción de gratitud"),
        ),
    ]
    return Camino(
        nombre="Evangelios",
        descripcion="Acompaña a Jesús y descubre cómo transforma cada encuentro.",
        capitulos=capitulos,
    )


def crear_camino_comunidad() -> Camino:
    capitulos = [
        Capitulo(
            titulo="Pentecostés y nueva comunidad",
            narrativa={
                MODO_CUENTO: (
                    "El Espíritu Santo llegó con viento y fuego. Todos se "
                    "escucharon y compartieron lo que tenían."
                ),
                MODO_ESTRATEGIA: (
                    "Pentecostés marca el nacimiento de una comunidad diversa "
                    "que comparte vida, enseñanza y recursos."
                ),
                MODO_REFLEXION: (
                    "La irrupción del Espíritu abre vínculos nuevos. La "
                    "comunidad cristiana nace como casa para todos."
                ),
            },
            pregunta="¿Qué práctica fue central en la primera comunidad cristiana?",
            opciones=[
                "A) Acumular bienes personales.",
                "B) Compartir y poner en común lo que tenían.",
                "C) Separarse por edades.",
                "D) Evitar comer juntos.",
            ],
            respuesta="B",
            pista="Piensa en una comunidad que vive como familia.",
            explicacion=(
                "Los discípulos perseveraban en la enseñanza, la oración y "
                "compartían los bienes para que nadie pasara necesidad."
            ),
            obstaculo="Puerta de Sabiduría: Construir comunidad en la unidad.",
            reflexion="Escribe una acción comunitaria que quieras impulsar.",
            recompensa=Recompensa(gemas=4, virtud="Paciencia",
                                  recuerdo="Postal: Icono de Pentecostés comunitario"),
        ),
        Capitulo(
            titulo="Cartas que animan",
            narrativa={
                MODO_CUENTO: (
                    "Pablo y otros líderes escribían cartas para animar, "
                    "corregir y recordar el amor de Dios."
                ),
                MODO_ESTRATEGIA: (
                    "Las epístolas fortalecían iglesias diversas, abordando "
                    "retos prácticos y teológicos."
                ),
                MODO_REFLEXION: (
                    "Leer las cartas apostólicas es escuchar una comunidad en "
                    "diálogo. Somos invitados a continuar esa conversación."
                ),
            },
            pregunta="¿Qué propósito tenían muchas cartas del Nuevo Testamento?",
            opciones=[
                "A) Dar recetas de cocina.",
                "B) Animar y orientar a las comunidades cristianas.",
                "C) Organizar viajes turísticos.",
                "D) Enseñar matemáticas.",
            ],
            respuesta="B",
            pista="Escucha el tono de acompañamiento fraterno.",
            explicacion=(
                "Las cartas buscaban sostener a las comunidades, resolver "
                "conflictos y profundizar en la fe."
            ),
            obstaculo="Puerta de Sabiduría: Escuchar y animar con la palabra escrita.",
            reflexion="¿A quién escribirías una carta de ánimo esta semana?",
            recompensa=Recompensa(gemas=4, virtud=None,
                                  recuerdo="Grabación: Lectura dramatizada de Filipenses"),
        ),
    ]
    return Camino(
        nombre="Comunidad",
        descripcion="Sumérgete en la vida de la iglesia naciente y su misión compartida.",
        capitulos=capitulos,
    )


CAMINOS = [
    crear_camino_patriarcas(),
    crear_camino_profetas(),
    crear_camino_evangelios(),
    crear_camino_comunidad(),
]

MISIONES_COMUNIDAD = [
    "Llama o envía un mensaje para animar a alguien que necesite compañía.",
    "Busca un versículo de esperanza y compártelo con tu familia.",
    "Prepara una nota de gratitud para alguien que sirve en tu comunidad.",
    "Dedica 10 minutos a orar por una persona mayor o un niño de tu entorno.",
]


def elegir_camino(disponibles: list[Camino]) -> Camino | None:
    print("\n=== Caminos disponibles ===")
    for idx, camino in enumerate(disponibles, start=1):
        print(f"{idx}. {camino.nombre} - {camino.descripcion}")
    print("0. Volver al menú principal")

    while True:
        eleccion = input("Elige un camino: ").strip()
        if eleccion == "0":
            return None
        if eleccion.isdigit():
            indice = int(eleccion) - 1
            if 0 <= indice < len(disponibles):
                return disponibles[indice]
        print("Opción no válida. Intenta nuevamente.")


def mostrar_virtudes(jugador: Jugador) -> None:
    print("\n=== Virtudes disponibles ===")
    for virtud, cantidad in jugador.virtudes.items():
        print(f"- {virtud}: {cantidad}")
    print("============================")


def aplicar_puerta_de_sabiduria(jugador: Jugador, capitulo: Capitulo) -> bool:
    print("\n" + capitulo.obstaculo)
    print("Responde la siguiente pregunta para avanzar.\n")
    print(envolver(capitulo.pregunta))
    for opcion in capitulo.opciones:
        print(opcion)

    intentos = 0
    while True:
        respuesta = input("Tu respuesta (letra): ").strip().upper()
        if not respuesta:
            print("Ingresa una letra.")
            continue
        intentos += 1
        if respuesta == capitulo.respuesta.upper():
            print("\n¡Correcto! " + capitulo.explicacion)
            return True

        print("\nRespuesta incorrecta.")
        if intentos >= 2:
            print("Puedes usar una virtud para obtener ayuda:")
            mostrar_virtudes(jugador)
            decision = input("¿Deseas usar 'Discernimiento' o 'Paciencia'? (s/n): ").strip().lower()
            if decision == "s":
                eleccion = input("Elige la virtud: ").strip().capitalize()
                if eleccion == "Discernimiento" and jugador.usar_virtud("Discernimiento"):
                    print("\nDiscernimiento activado. Pista:", capitulo.pista)
                elif eleccion == "Paciencia" and jugador.usar_virtud("Paciencia"):
                    print("\nPaciencia activada. Tómate tu tiempo para pensar otra vez.")
                else:
                    print("No puedes usar esa virtud ahora.")
            else:
                print("Respira hondo y vuelve a intentarlo.")
        else:
            print("Intenta nuevamente. Confía, puedes lograrlo.")


def entregar_recompensas(jugador: Jugador, capitulo: Capitulo) -> None:
    recompensa = capitulo.recompensa
    if recompensa.gemas:
        jugador.ganar_gemas(recompensa.gemas)
        print(f"\nHas ganado {recompensa.gemas} Gemas de Esperanza. "
              f"Total actual: {jugador.gemas}.")
    if recompensa.virtud:
        jugador.ganar_virtud(recompensa.virtud)
        print(f"Recibiste la virtud '{recompensa.virtud}' para apoyar a otros caminos.")
    if recompensa.recuerdo:
        print("\nCofre de Recuerdos abierto:")
        print(envolver(recompensa.recuerdo))


def registrar_reflexion(jugador: Jugador, camino: Camino, capitulo: Capitulo) -> None:
    print("\nÁrbol de Testimonios - Comparte algo breve.")
    print(envolver(capitulo.reflexion))
    reflexion = input("Escribe tu respuesta (o pulsa Enter para omitir): ").strip()
    if reflexion:
        jugador.registrar_testimonio(camino.nombre, capitulo.titulo, reflexion)
        print("Tu testimonio ha sido añadido al Árbol de Testimonios.")
    else:
        print("Tal vez más adelante quieras dejar un testimonio.")


def recorrer_camino(jugador: Jugador, camino: Camino) -> None:
    print(f"\n*** Inicias el camino de {camino.nombre} ***")
    for capitulo in camino.capitulos:
        print(f"\n--- {capitulo.titulo} ---")
        relato = capitulo.narrativa.get(jugador.modo, capitulo.narrativa[MODO_CUENTO])
        print(envolver(relato))

        if not aplicar_puerta_de_sabiduria(jugador, capitulo):
            # La función siempre retorna True, pero dejamos el bloque por claridad.
            break

        entregar_recompensas(jugador, capitulo)
        registrar_reflexion(jugador, camino, capitulo)

    print(f"\nCamino {camino.nombre} completado. Respira y celebra lo aprendido.")


def mostrar_arbol_testimonios(jugador: Jugador) -> None:
    print("\n=== Árbol de Testimonios Familiar ===")
    if not jugador.testimonios:
        print("Todavía no hay testimonios. Cada capítulo ofrece la oportunidad de añadir uno.")
        return
    for idx, registro in enumerate(jugador.testimonios, start=1):
        print(f"{idx}. {registro['camino']} / {registro['capitulo']}")
        print("   " + envolver(registro["texto"]))
    print("=====================================")


def activar_mision_comunidad(jugador: Jugador) -> None:
    mision = random.choice(MISIONES_COMUNIDAD)
    print("\n=== Misión de Comunidad ===")
    print(envolver(mision))
    decision = input("¿Te comprometes a intentarlo hoy? (s/n): ").strip().lower()
    if decision == "s":
        jugador.ganar_gemas(2)
        if jugador.usar_virtud("Servicio"):
            print("\nHas usado la virtud 'Servicio' para animar a otros.")
        else:
            print("\nAún no tenías la virtud 'Servicio', ¡recibe una por tu disposición!")
            jugador.ganar_virtud("Servicio")
        print("Recibes 2 Gemas de Esperanza por tu compromiso. ¡Gracias por servir!")
    else:
        print("Quizá otro día. La misión seguirá esperándote.")


def mostrar_estado(jugador: Jugador) -> None:
    print("\n=== Estado Actual ===")
    print(f"Jugador: {jugador.nombre} | Grupo: {jugador.grupo_edad} | Modo: {jugador.modo}")
    print(f"Gemas de Esperanza: {jugador.gemas}")
    print("Virtudes:")
    for virtud, cantidad in jugador.virtudes.items():
        print(f"  - {virtud}: {cantidad}")
    print("======================")


def solicitar_datos_jugador() -> Jugador:
    print("Bienvenido a Senderos de Luz 🌟")
    nombre = input("¿Cómo te llamas? ").strip() or "Peregrino"

    print("\nElige tu grupo de edad (esto ajusta el acompañamiento):")
    grupos = ["Niño", "Adulto", "Anciano"]
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo}")
    while True:
        eleccion = input("Tu opción: ").strip()
        if eleccion.isdigit():
            indice = int(eleccion) - 1
            if 0 <= indice < len(grupos):
                grupo_edad = grupos[indice]
                break
        print("Selecciona una opción válida (1-3).")

    print("\nElige tu modo de viaje espiritual:")
    modos = [
        (MODO_CUENTO, "Modo cuento ilustrado (lectura breve y lenguaje sencillo)."),
        (MODO_ESTRATEGIA, "Modo estrategia ligera (más detalles y retos)."),
        (MODO_REFLEXION, "Modo reflexión profunda (enfoque contemplativo)."),
    ]
    for idx, (_, descripcion) in enumerate(modos, start=1):
        print(f"{idx}. {descripcion}")

    while True:
        eleccion = input("Tu opción: ").strip()
        if eleccion.isdigit():
            indice = int(eleccion) - 1
            if 0 <= indice < len(modos):
                modo = modos[indice][0]
                break
        print("Selecciona una opción válida (1-3).")

    print("\nRecibes un mazo inicial de virtudes y 1 Gema de Esperanza por tu valentía.")
    jugador = Jugador(nombre=nombre, grupo_edad=grupo_edad, modo=modo)
    jugador.ganar_gemas(1)
    return jugador


def menu_principal(jugador: Jugador) -> None:
    while True:
        print("\n=== Menú Principal ===")
        print("1. Recorrer un camino bíblico")
        print("2. Ver Árbol de Testimonios")
        print("3. Activar una Misión de Comunidad")
        print("4. Mostrar estado actual")
        print("5. Salir del juego")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            camino = elegir_camino(CAMINOS)
            if camino:
                recorrer_camino(jugador, camino)
        elif opcion == "2":
            mostrar_arbol_testimonios(jugador)
        elif opcion == "3":
            activar_mision_comunidad(jugador)
        elif opcion == "4":
            mostrar_estado(jugador)
        elif opcion == "5":
            print("\nGracias por caminar por Senderos de Luz. ¡Hasta pronto!")
            break
        else:
            print("Opción no reconocida. Intenta de nuevo.")


def main() -> None:
    jugador = solicitar_datos_jugador()
    menu_principal(jugador)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJuego interrumpido. Que la paz te acompañe.")
        sys.exit(0)
