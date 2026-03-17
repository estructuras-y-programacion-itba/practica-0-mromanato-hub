import random
from collections import Counter

# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
CATEGORIAS = {
    "1": "Unos",
    "2": "Doses",
    "3": "Treses",
    "4": "Cuatros",
    "5": "Cincos",
    "6": "Seises",
    "E": "Escalera",
    "F": "Full",
    "P": "Póker",
    "G": "Generala",
    "S": "Servida",   # alias interno – no existe como input del jugador
}

PUNTOS_BASE = {
    "E": 20,
    "F": 30,
    "P": 40,
    "G": 50,
}

SEPARADOR = "=" * 60


# ─────────────────────────────────────────────
#  DADOS
# ─────────────────────────────────────────────
def tirar_dados(cantidad: int) -> list[int]:
    """Devuelve una lista de `cantidad` valores aleatorios entre 1 y 6."""
    return [random.randint(1, 6) for _ in range(cantidad)]


def mostrar_dados(dados: list[int], indices_guardados: list[int] = None) -> None:
    """Imprime los dados numerados, marcando los que están guardados."""
    indices_guardados = indices_guardados or []
    print("\n  Pos:  ", end="")
    for i in range(len(dados)):
        print(f"[{i+1}]", end="  ")
    print()
    print("  Dado: ", end="")
    for i, d in enumerate(dados):
        marcador = f" {d} " if i not in indices_guardados else f"*{d}*"
        print(marcador, end="  ")
    print()
    if indices_guardados:
        print("  (* = guardado)")


# ─────────────────────────────────────────────
#  EVALUACIÓN DE JUGADAS
# ─────────────────────────────────────────────
def es_escalera(dados: list[int]) -> bool:
    return sorted(dados) == [1, 2, 3, 4, 5] or sorted(dados) == [2, 3, 4, 5, 6]


def es_full(dados: list[int]) -> bool:
    conteo = Counter(dados).values()
    return sorted(conteo) == [2, 3]


def es_poker(dados: list[int]) -> bool:
    return max(Counter(dados).values()) >= 4


def es_generala(dados: list[int]) -> bool:
    return len(set(dados)) == 1


def suma_numero(dados: list[int], numero: int) -> int:
    return sum(d for d in dados if d == numero)


def jugadas_validas(dados: list[int], planilla: dict) -> dict:
    """
    Devuelve un dict {código: puntaje} de las categorías que el jugador
    aún no usó y en las que podría anotar algo (> 0).
    """
    validas = {}
    for cat in planilla:
        if planilla[cat] is not None:          # ya usada
            continue
        if cat in "123456":
            pts = suma_numero(dados, int(cat))
            if pts > 0:
                validas[cat] = pts
        elif cat == "E" and es_escalera(dados):
            validas["E"] = PUNTOS_BASE["E"]
        elif cat == "F" and es_full(dados):
            validas["F"] = PUNTOS_BASE["F"]
        elif cat == "P" and es_poker(dados):
            validas["P"] = PUNTOS_BASE["P"]
        elif cat == "G" and es_generala(dados):
            validas["G"] = PUNTOS_BASE["G"]
    return validas


def categorias_pendientes(planilla: dict) -> list[str]:
    return [c for c, v in planilla.items() if v is None]


# ─────────────────────────────────────────────
#  PLANILLA
# ─────────────────────────────────────────────
def nueva_planilla() -> dict:
    """Crea la planilla vacía de un jugador (None = no usada)."""
    return {cat: None for cat in ["1", "2", "3", "4", "5", "6", "E", "F", "P", "G", "S"]}


def mostrar_planilla(nombre: str, planilla: dict) -> None:
    """Muestra la planilla de un jugador."""
    print(f"\n  Planilla de {nombre}:")
    etiquetas = {
        "1": "Unos       ",
        "2": "Doses      ",
        "3": "Treses     ",
        "4": "Cuatros    ",
        "5": "Cincos     ",
        "6": "Seises     ",
        "E": "Escalera   ",
        "F": "Full       ",
        "P": "Póker      ",
        "G": "Generala   ",
        "S": "Servida    ",
    }
    for cat, etiq in etiquetas.items():
        val = planilla[cat]
        estado = f"{val:>4}" if val is not None else "  --"
        print(f"    [{cat}] {etiq}: {estado}")
    total = sum(v for v in planilla.values() if v is not None)
    print(f"    {'─'*22}")
    print(f"    TOTAL          : {total:>4}")


def puntaje_total(planilla: dict) -> int:
    return sum(v for v in planilla.values() if v is not None)


def planilla_completa(planilla: dict) -> bool:
    return all(v is not None for v in planilla.values())


# ─────────────────────────────────────────────
#  INTERACCIÓN CON EL JUGADOR
# ─────────────────────────────────────────────
def pedir_dados_a_guardar(dados: list[int], indices_guardados: list[int]) -> list[int]:
    """
    Pregunta al jugador qué dados quiere guardar (o todos / ninguno).
    Devuelve la lista actualizada de índices guardados.
    """
    while True:
        print("\n  ¿Qué dados querés guardar? (ingresá las posiciones separadas por espacios,")
        print("  'T' para guardar todos o Enter para no guardar ninguno y volver a tirar todos)")
        entrada = input("  > ").strip().upper()

        if entrada == "T":
            return list(range(5))
        if entrada == "":
            return []

        try:
            elegidos = [int(x) - 1 for x in entrada.split()]
            if all(0 <= e <= 4 for e in elegidos):
                return elegidos
            else:
                print("  ⚠ Posiciones inválidas. Usá números del 1 al 5.")
        except ValueError:
            print("  ⚠ Entrada inválida. Ingresá números, 'T' o Enter.")


def elegir_categoria(dados: list[int], planilla: dict, es_primera_tirada: bool) -> tuple[str, int]:
    """
    Muestra las opciones disponibles y devuelve (categoría, puntaje_final).
    Si no hay jugadas válidas, el jugador debe anotar 0 en una categoría pendiente.
    """
    validas = jugadas_validas(dados, planilla)
    pendientes = categorias_pendientes(planilla)

    etiquetas = {
        "1": "Unos", "2": "Doses", "3": "Treses",
        "4": "Cuatros", "5": "Cincos", "6": "Seises",
        "E": "Escalera (20 pts)", "F": "Full (30 pts)",
        "P": "Póker (40 pts)", "G": "Generala (50 pts)",
        "S": "Servida (25 pts)",
    }

    print("\n  Categorías disponibles:")
    if validas:
        for cat, pts in validas.items():
            extra = ""
            if es_primera_tirada and cat in ("E", "F", "P"):
                extra = f" + 5 bonus = {pts + 5}"
            elif es_primera_tirada and cat == "G":
                extra = " + 30 bonus (¡GENERALA REAL!)"
            print(f"    [{cat}] {etiquetas.get(cat, cat)}: {pts}{extra}")
    else:
        print("    (ninguna jugada válida — debés anotar 0 en una categoría pendiente)")

    # Opción "Servida": solo si la categoría S está libre y hay una jugada EPFG válida
    puede_servida = (
        planilla.get("S") is None
        and not es_primera_tirada  # la Servida no aplica en primera tirada como categoría especial
        and any(cat in validas for cat in ("E", "F", "P", "G"))
        and "S" in pendientes
    )
    if puede_servida:
        print(f"    [S] Servida (25 pts fijos si tenés E/F/P/G)")

    print("\n  Categorías pendientes:", ", ".join(pendientes))

    while True:
        opcion = input("\n  Elegí una categoría: ").strip().upper()

        # Sin jugadas válidas → solo puede anotar 0 en una pendiente
        if not validas:
            if opcion in pendientes:
                return opcion, 0
            print("  ⚠ Elegí una de las categorías pendientes.")
            continue

        # Opción Servida
        if opcion == "S" and puede_servida:
            return "S", 25

        if opcion not in pendientes:
            print("  ⚠ Esa categoría no está disponible o ya fue usada.")
            continue

        # Categorías numéricas
        if opcion in "123456":
            pts = suma_numero(dados, int(opcion))
            return opcion, pts

        # Categorías especiales — debe ser válida
        if opcion in ("E", "F", "P", "G"):
            if opcion not in validas:
                print(f"  ⚠ No tenés {etiquetas[opcion]} con estos dados.")
                continue
            pts = PUNTOS_BASE[opcion]
            if es_primera_tirada:
                if opcion == "G":
                    pts += 30
                else:
                    pts += 5
            return opcion, pts

        print("  ⚠ Opción inválida.")


# ─────────────────────────────────────────────
#  TURNO DE UN JUGADOR
# ─────────────────────────────────────────────
def jugar_turno(nombre: str, planilla: dict) -> tuple[bool, str, int]:
    """
    Ejecuta el turno completo de un jugador.
    Devuelve (generala_real: bool, categoria_elegida: str, puntaje: int).
    """
    print(f"\n{SEPARADOR}")
    print(f"  TURNO DE {nombre.upper()}")
    print(SEPARADOR)

    dados = tirar_dados(5)
    indices_guardados: list[int] = []
    es_primera = True
    tirada_actual = 1

    while True:
        print(f"\n  — Tirada {tirada_actual} —")
        mostrar_dados(dados, indices_guardados)

        # ¿Generala Real en primera tirada?
        if es_primera and es_generala(dados):
            print("\n  🎲 ¡¡GENERALA REAL!! Victoria automática.")
            pts = PUNTOS_BASE["G"] + 30
            planilla["G"] = pts
            return True, "G", pts

        # Si llegó a la tercera tirada → elige categoría directamente
        if tirada_actual == 3:
            print("\n  (Última tirada alcanzada — elegí categoría)")
            cat, pts = elegir_categoria(dados, planilla, es_primera)
            planilla[cat] = pts
            print(f"\n  ✔ Anotaste '{CATEGORIAS.get(cat, cat)}' con {pts} puntos.")
            return False, cat, pts

        # Pregunta si quiere volver a tirar
        print("\n  ¿Querés volver a tirar? (S/N)")
        resp = input("  > ").strip().upper()
        if resp != "S":
            cat, pts = elegir_categoria(dados, planilla, es_primera)
            planilla[cat] = pts
            print(f"\n  ✔ Anotaste '{CATEGORIAS.get(cat, cat)}' con {pts} puntos.")
            return False, cat, pts

        # El jugador elige qué dados guardar
        indices_guardados = pedir_dados_a_guardar(dados, indices_guardados)

        # Si guardó todos → no tiene sentido tirar
        if len(indices_guardados) == 5:
            print("\n  (Guardaste todos los dados — elegí categoría)")
            cat, pts = elegir_categoria(dados, planilla, es_primera)
            planilla[cat] = pts
            print(f"\n  ✔ Anotaste '{CATEGORIAS.get(cat, cat)}' con {pts} puntos.")
            return False, cat, pts

        # Re-tirar los dados no guardados
        nuevos_dados = tirar_dados(5 - len(indices_guardados))
        dados_tirada = []
        nuevo_idx = 0
        for i in range(5):
            if i in indices_guardados:
                dados_tirada.append(dados[i])
            else:
                dados_tirada.append(nuevos_dados[nuevo_idx])
                nuevo_idx += 1
        dados = dados_tirada

        es_primera = False
        tirada_actual += 1


# ─────────────────────────────────────────────
#  MARCADOR Y RESUMEN
# ─────────────────────────────────────────────
def mostrar_marcador(jugadores: list[str], planillas: list[dict]) -> None:
    print(f"\n{SEPARADOR}")
    print("  MARCADOR ACTUAL")
    print(SEPARADOR)
    for nombre, planilla in zip(jugadores, planillas):
        mostrar_planilla(nombre, planilla)


def determinar_ganador(jugadores: list[str], planillas: list[dict]) -> None:
    print(f"\n{SEPARADOR}")
    print("  RESULTADO FINAL")
    print(SEPARADOR)
    totales = [(nombre, puntaje_total(p)) for nombre, p in zip(jugadores, planillas)]
    for nombre, total in totales:
        print(f"  {nombre}: {total} puntos")
    max_pts = max(t for _, t in totales)
    ganadores = [n for n, t in totales if t == max_pts]
    print()
    if len(ganadores) == 1:
        print(f"  🏆 ¡Ganó {ganadores[0]} con {max_pts} puntos!")
    else:
        print(f"  🤝 ¡Empate entre {' y '.join(ganadores)} con {max_pts} puntos!")
    print(SEPARADOR)


# ─────────────────────────────────────────────
#  CONFIGURACIÓN INICIAL
# ─────────────────────────────────────────────
def pedir_nombre(numero: int) -> str:
    while True:
        nombre = input(f"  Nombre del Jugador {numero}: ").strip()
        if nombre:
            return nombre
        print("  ⚠ El nombre no puede estar vacío.")


# ─────────────────────────────────────────────
#  BUCLE PRINCIPAL
# ─────────────────────────────────────────────
def main() -> None:
    print(SEPARADOR)
    print("       🎲  JUEGO DE LA GENERALA  🎲")
    print(SEPARADOR)
    print("\n  Ingresá los nombres de los jugadores:")
    jugadores = [pedir_nombre(1), pedir_nombre(2)]
    planillas = [nueva_planilla(), nueva_planilla()]

    turno = 0          # 0 o 1 → índice del jugador actual
    generala_real = False

    while True:
        nombre = jugadores[turno]
        planilla = planillas[turno]

        es_gr, cat, pts = jugar_turno(nombre, planilla)

        if es_gr:
            generala_real = True
            mostrar_marcador(jugadores, planillas)
            print(f"\n  ¡{nombre} obtuvo una Generala Real! El juego termina.")
            break

        mostrar_marcador(jugadores, planillas)

        # Verificar si ambos completaron la planilla
        if all(planilla_completa(p) for p in planillas):
            print("\n  ¡Ambos jugadores completaron todas las categorías!")
            break

        # Pasar al siguiente jugador
        turno = 1 - turno

        input("\n  Presioná Enter para continuar al siguiente turno...")

    determinar_ganador(jugadores, planillas)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
