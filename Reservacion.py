"""
@file Reservacion.py
@author Stratatek Software Solutions
@brief Sitema de Reservación de Mesas en/para un Restaurante.

@version 0.5
@date 2025-07-02

@copyright Copyright (c) 2025
"""
# Reservacion.py



import datetime

# =======================================================================================
# Módulo: datetime
# Propósito: Este módulo proporciona clases para trabajar con fechas y horas.
# Es crucial para validar formatos de fecha, realizar comparaciones y otras
# operaciones temporales de manera robusta, en lugar de manejar fechas
# como simples cadenas de texto que no ofrecen validación inherente.
# =======================================================================================

# --- CLASES DEL MODELO DE NEGOCIO ---
# Estas clases representan las entidades principales de nuestro sistema de reservas
# y encapsulan su estado y comportamiento.

class MesaBase:
    """
    ===================================================================================
    Clase MesaBase: Base para la Abstracción y Herencia de Mesas
    -----------------------------------------------------------------------------------
    Propósito: Define las características y comportamientos fundamentales que
               cualquier tipo de mesa en el restaurante debe tener. Actúa como
               la clase base para otras especializaciones de mesas (General, VIP).
    Principios POO:
        - Abstracción: Oculta los detalles internos de cómo se gestiona la
                       disponibilidad de una mesa (a través del diccionario
                       'disponibilidad'). Proporciona una interfaz simple para
                       reservar, liberar y verificar disponibilidad.
        - Encapsulamiento:
            - **Atributos:**
                - `self.numero`: **Público**. Accesible directamente para consulta.
                - `self.disponibilidad`: **Gestionado/Semi-público**. No tiene un guion bajo,
                  pero su manipulación está estrictamente controlada por los métodos
                  de la clase (`inicializar_dia`, `reservar_hora`, `liberar_hora`).
                  Aunque es accesible directamente, se espera que los desarrolladores
                  lo modifiquen solo a través de los métodos proporcionados para
                  mantener la integridad.
            - **Métodos (Getters y Setters implícitos/explícitos):**
                - `__init__`, `__str__`: Públicos.
                - `inicializar_dia(fecha_str, horario_inicio, horario_fin)`: Actúa como un **setter**
                  controlado para la parte de `self.disponibilidad` correspondiente a un día.
                  Asegura que el día se prepare correctamente antes de cualquier operación.
                - `reservar_hora(fecha_str, hora, horario_inicio, horario_fin)`: Actúa como un **setter**
                  específico. Modifica el estado de disponibilidad de una hora a "reservado".
                  Es un setter porque cambia el estado interno de la mesa.
                  Incorpora validación interna (si la hora está disponible).
                - `liberar_hora(fecha_str, hora)`: Actúa como un **setter** específico.
                  Modifica el estado de disponibilidad de una hora a "disponible".
                  También es un setter que controla el cambio de estado.
                - `esta_disponible(fecha_str, hora, horario_inicio, horario_fin)`: Actúa como un **getter**
                  explícito. Su propósito es únicamente consultar el estado de un recurso
                  interno (`self.disponibilidad`) sin modificarlo. No toma argumentos para el nuevo valor.
                - `es_vip_mesa()`: Actúa como un **getter** abstracto. Su propósito es consultar
                  una propiedad de la mesa (si es VIP) de manera polimórfica.
    ===================================================================================
    """

    def __init__(self, numero):
        """
        Constructor de la clase MesaBase.
        Args:
            numero (int): El número identificador único de la mesa.
        """
        self.numero = numero
        self.disponibilidad = {}

    def __str__(self):
        """
        Método especial (dunder method): Define la representación en cadena del objeto.
        Este será sobrescrito por las clases hijas para añadir especificidad.
        """
        return f"Mesa {self.numero}"

    def inicializar_dia(self, fecha_str, horario_inicio, horario_fin):
        """
        Actúa como un Setter Controlado: Inicializa la estructura de disponibilidad para un día.
        """
        if fecha_str not in self.disponibilidad:
            self.disponibilidad[fecha_str] = {hora: True for hora in range(horario_inicio, horario_fin + 1)}

    def reservar_hora(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Actúa como un Setter de Estado: Modifica la disponibilidad de una hora a False (reservado).
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        if hora in self.disponibilidad[fecha_str] and self.disponibilidad[fecha_str][hora]:
            self.disponibilidad[fecha_str][hora] = False
            return True
        return False

    def liberar_hora(self, fecha_str, hora):
        """
        Actúa como un Setter de Estado: Modifica la disponibilidad de una hora a True (disponible).
        """
        if fecha_str in self.disponibilidad and hora in self.disponibilidad[fecha_str]:
            self.disponibilidad[fecha_str][hora] = True
            return True
        return False

    def esta_disponible(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Actúa como un Getter: Consulta el estado de disponibilidad sin modificarlo.
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        return self.disponibilidad.get(fecha_str, {}).get(hora, False)

    def es_vip_mesa(self):
        """
        Actúa como un Getter (abstracto): Consulta si la mesa es VIP.
        """
        raise NotImplementedError("Las subclases deben implementar este método para indicar si son VIP.")


class MesaGeneral(MesaBase):
    """
    ===================================================================================
    Clase MesaGeneral: Especialización de Mesa para Zonas Generales
    -----------------------------------------------------------------------------------
    Tipo de Herencia: Herencia Simple (o Monohilo).
    Qué Hereda de MesaBase: Atributos (`numero`, `disponibilidad`) y métodos
    (`inicializar_dia()`, `reservar_hora()`, `liberar_hora()`, `esta_disponible()`).

    Principios POO:
        - Herencia: `MesaGeneral` "es un tipo de" `MesaBase`.
        - Polimorfismo: Sobreescribe `__str__` y `es_vip_mesa`.
        - Encapsulamiento:
            - Hereda el encapsulamiento de `MesaBase`.
            - `__str__`, `es_vip_mesa`: Actúan como **getters** públicos sobrescritos.
    ===================================================================================
    """
    def __init__(self, numero):
        super().__init__(numero)

    def __str__(self):
        return f"Mesa {self.numero} (General)"

    def es_vip_mesa(self):
        return False


class MesaVIP(MesaBase):
    """
    ===================================================================================
    Clase MesaVIP: Especialización de Mesa para Zonas VIP
    -----------------------------------------------------------------------------------
    Tipo de Herencia: Herencia Simple (o Monohilo).
    Qué Hereda de MesaBase: Atributos (`numero`, `disponibilidad`) y métodos
    (`inicializar_dia()`, `reservar_hora()`, `liberar_hora()`, `esta_disponible()`).

    Principios POO:
        - Herencia: `MesaVIP` "es un tipo de" `MesaBase`.
        - Polimorfismo: Sobreescribe `__str__` y `es_vip_mesa`.
        - Encapsulamiento:
            - Hereda el encapsulamiento de `MesaBase`.
            - `__str__`, `es_vip_mesa`: Actúan como **getters** públicos sobrescritos.
    ===================================================================================
    """
    def __init__(self, numero):
        super().__init__(numero)

    def __str__(self):
        return f"Mesa {self.numero} (VIP)"

    def es_vip_mesa(self):
        return True


class Reserva:
    """
    ===================================================================================
    Clase Reserva: Representa una reservación individual.
    -----------------------------------------------------------------------------------
    Principios POO:
        - Encapsulamiento:
            - **Atributos:**
                - `cliente_nombre`, `fecha_str`, `hora`, `mesa`, `folio`: Todos son **públicos**.
                  Aunque `folio` se genera internamente, es parte de la información
                  que se espera sea accesible para identificar la reserva.
            - **Métodos (Getters y Setters):**
                - `__init__`, `__str__`: Públicos.
                - `_generar_folio`: **Protegido (por convención)**. Es un **setter implícito**
                  ya que asigna un valor al atributo `self.folio` durante la inicialización.
                  La lógica de cómo se calcula el folio está encapsulada aquí.
                  No hay setters explícitos para cambiar el `cliente_nombre`, `fecha_str`,
                  `hora`, `mesa`, o `folio` una vez que la `Reserva` ha sido creada,
                  lo que implica que son atributos de solo lectura después de la inicialización,
                  garantizando la inmutabilidad de la reserva.
        - Abstracción: Oculta los detalles de cómo se genera el folio.
    ===================================================================================
    """

    def __init__(self, cliente_nombre, fecha_str, hora, mesa):
        """
        Constructor de la clase Reserva.
        Args:
            cliente_nombre (str): Nombre del cliente.
            fecha_str (str): Fecha de la reserva.
            hora (int): Hora de la reserva.
            mesa (MesaBase): El objeto Mesa (MesaGeneral o MesaVIP) asociado.
        """
        self.cliente_nombre = cliente_nombre
        self.fecha_str = fecha_str
        self.hora = hora
        self.mesa = mesa
        self.folio = self._generar_folio() # El folio se asigna al atributo 'folio'.

    def _generar_folio(self):
        """
        Actúa como un Setter Implícito para 'self.folio'.
        Genera y asigna el valor al atributo 'folio' durante la construcción del objeto.
        """
        prefijo = "VX" if self.mesa.es_vip_mesa() else "GX"
        return f"{prefijo}{self.mesa.numero}"

    def __str__(self):
        return (f"Reserva para {self.cliente_nombre} "
                f"en {self.mesa} el {self.fecha_str} a las {self.hora}:00. Folio: {self.folio}")


class Restaurante:
    """
    ===================================================================================
    Clase Restaurante: El Sistema de Gestión de Reservas Principal
    -----------------------------------------------------------------------------------
    Principios POO:
        - Encapsulamiento:
            - **Atributos:**
                - `mesas`, `reservas`, `horario_inicio`, `horario_fin`: Todos son **públicos**.
                  Aunque son accesibles, la manipulación de `mesas` y `reservas` está
                  diseñada para hacerse a través de los métodos de la clase
                  (`hacer_reservacion`, `eliminar_reservacion`) para mantener la
                  integridad del sistema. No hay setters directos para estas listas;
                  se modifican mediante métodos de negocio.
            - **Métodos (Getters y Setters):**
                - `__init__`: Público.
                - `_validar_hora(hora)`: Actúa como un **getter de validación**.
                  Consulta una condición (`hora` en rango) sin modificar el estado.
                - `_validar_fecha(fecha_str)`: Actúa como un **getter de validación**.
                  Consulta la validez del formato de fecha sin modificar el estado.
                - `ver_disponibilidad(fecha_str)`: Actúa principalmente como un **getter de información**
                  complejo. Recopila y muestra información de disponibilidad
                  sin modificar el estado del `Restaurante` o de las `Mesa`s
                  (más allá de la inicialización de días si es necesaria).
                - `hacer_reservacion(cliente_nombre, fecha_str, hora, numero_mesa)`:
                  Actúa como un **setter de estado complejo**. Modifica el estado interno
                  del restaurante al añadir una `Reserva` a `self.reservas` y al
                  modificar la disponibilidad de una `Mesa` a través de su método `reservar_hora`.
                - `eliminar_reservacion(fecha_str, hora, folio_mesa)`:
                  Actúa como un **setter de estado complejo**. Modifica el estado interno
                  del restaurante al eliminar una `Reserva` de `self.reservas` y al
                  modificar la disponibilidad de una `Mesa` a través de su método `liberar_hora`.
        - Abstracción: Proporciona una interfaz de alto nivel para los casos de uso.
        - Polimorfismo: Gestiona objetos de `MesaGeneral` y `MesaVIP` de manera
                        uniforme a través de su clase base `MesaBase`.
    ===================================================================================
    """

    def __init__(self):
        self.mesas = []
        for i in range(1, 6):
            self.mesas.append(MesaGeneral(i))
        for i in range(1, 6):
            self.mesas.append(MesaVIP(5 + i))

        self.reservas = []
        self.horario_inicio = 13
        self.horario_fin = 16

    def _validar_hora(self, hora):
        return self.horario_inicio <= hora <= self.horario_fin

    def _validar_fecha(self, fecha_str):
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def ver_disponibilidad(self, fecha_str):
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use el formato adecuado: YY-MM-DD.")
            return

        print(f"\n--- Disponibilidad para el {fecha_str} ---")
        disponibilidad_encontrada = False

        for mesa in sorted(self.mesas, key=lambda m: (not m.es_vip_mesa(), m.numero)):
            mesa.inicializar_dia(fecha_str, self.horario_inicio, self.horario_fin)
            print(f"\n{mesa}:")
            horas_disponibles_mesa = []
            for hora in range(self.horario_inicio, self.horario_fin + 1):
                estado = "Disponible" if mesa.esta_disponible(fecha_str, hora, self.horario_inicio, self.horario_fin) else "Reservado"
                horas_disponibles_mesa.append(f" {hora}:00-{hora+1}:00 -> {estado}")
                disponibilidad_encontrada = True
            print("".join(horas_disponibles_mesa))

        if not disponibilidad_encontrada:
            print("No hay información de disponibilidad para las mesas en esta fecha.")
        print("---------------------------------")

    def hacer_reservacion(self, cliente_nombre, fecha_str, hora, numero_mesa):
        if not all([cliente_nombre, fecha_str, hora, numero_mesa]):
            print("❌ Error: La reservación no se guarda porque faltan datos. Por favor, complete todos los campos.")
            return None

        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. UsebeginPath-MM-DD.")
            return None
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario de reservas es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return None

        mesa_seleccionada = None
        for mesa in self.mesas:
            if mesa.numero == numero_mesa:
                mesa_seleccionada = mesa
                break

        if not mesa_seleccionada:
            print(f"❌ Error: Mesa {numero_mesa} no encontrada.")
            return None

        if not mesa_seleccionada.esta_disponible(fecha_str, hora, self.horario_inicio, self.horario_fin):
            print(f"❌ Error: La mesa {numero_mesa} no está disponible el {fecha_str} a las {hora}:00.")
            return None

        if mesa_seleccionada.reservar_hora(fecha_str, hora, self.horario_inicio, self.horario_fin):
            nueva_reserva = Reserva(cliente_nombre, fecha_str, hora, mesa_seleccionada)
            self.reservas.append(nueva_reserva)
            print(f"✅ ¡Reservación exitosa! {nueva_reserva}")
            return nueva_reserva
        else:
            print("❌ Error inesperado al intentar reservar la mesa.")
            return None

    def eliminar_reservacion(self, fecha_str, hora, folio_mesa):
        if not all([fecha_str, hora, folio_mesa]):
            print("❌ Error: Por favor, complete todos los datos para eliminar la reserva.")
            return False

        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use el formato adecuado: YY-MM-DD.")
            return False
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario de reservas es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return False

        reserva_encontrada = None
        for reserva in self.reservas:
            if (reserva.folio == folio_mesa and
                reserva.fecha_str == fecha_str and
                reserva.hora == hora):
                reserva_encontrada = reserva
                break

        if not reserva_encontrada:
            print(f"❌ Error: No se encontró una reservación con el folio '{folio_mesa}' "
                  f"para el {fecha_str} a las {hora}:00.")
            return False

        confirmacion = input(f"¿Está seguro que desea eliminar la reserva de {reserva_encontrada.cliente_nombre} "
                             f"para {reserva_encontrada.mesa} el {reserva_encontrada.fecha_str} a las {reserva_encontrada.hora}:00? (s/n): ").lower()
        if confirmacion != 's':
            print("🚫 Eliminación cancelada.")
            return False

        self.reservas.remove(reserva_encontrada)
        reserva_encontrada.mesa.liberar_hora(fecha_str, hora)
        print(f"✅ Reservación para '{reserva_encontrada.cliente_nombre}' eliminada exitosamente.")
        return True

# --- SIMULACIÓN DE LA INTERACCIÓN DEL EMPLEADO (PROGRAMA PRINCIPAL) ---

def mostrar_menu():
    print("\n--- Menú del Sistema de Reservas ---")
    print("1. Ver Disponibilidad")
    print("2. Hacer Reservación")
    print("3. Eliminar Reservación")
    print("4. Salir")
    print("-----------------------------------")

if __name__ == "__main__":
    restaurante = Restaurante()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            fecha_disp = input("Ingrese la fecha para ver disponibilidad (YYYY-MM-DD): ")
            restaurante.ver_disponibilidad(fecha_disp)

        elif opcion == '2':
            print("\n--- Hacer Reservación ---")
            cliente_nombre = input("Nombre del cliente: ")
            fecha_reserva = input("Fecha de la reserva (YYYY-MM-DD): ")
            try:
                hora_reserva = int(input(f"Hora de la reserva ({restaurante.horario_inicio}-{restaurante.horario_fin}): "))
            except ValueError:
                print("❌ Hora inválida. Debe ser un número entero.")
                continue
            try:
                numero_mesa = int(input("Número de mesa deseada: "))
            except ValueError:
                print("❌ Número de mesa inválido. Debe ser un número entero.")
                continue

            restaurante.hacer_reservacion(cliente_nombre, fecha_reserva, hora_reserva, numero_mesa)

        elif opcion == '3':
            print("\n--- Eliminar Reservación ---")
            folio_eliminar = input("Folio de la reserva a eliminar (ej. VX1, GX2): ")
            fecha_eliminar = input("Fecha de la reserva (YYYY-MM-DD): ")
            try:
                hora_eliminar = int(input(f"Hora de la reserva ({restaurante.horario_inicio}-{restaurante.horario_fin}): "))
            except ValueError:
                print("❌ Hora inválida. Debe ser un número entero.")
                continue

            restaurante.eliminar_reservacion(fecha_eliminar, hora_eliminar, folio_eliminar)

        elif opcion == '4':
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")
