"""
@file reservacion.py
@author A.G.R
@brief Sitema de Reservaciones de mesas para un Restaurante.

@version 0.1
@date 2025-07-02

@copyright Copyright (c) 2025
"""
# Reservacion.py



import datetime

# Importa la biblioteca datetime para manejar fechas y horas (necesario para las reservaciones).
# Es mucho mejor que usar solo cadenas de carácteres para validaciones y operaciones con fechas.


class Mesa:
    """
    Clase Mesa: Representa una mesa individual en el restaurante.
    Encapsulamiento: Agrupa los datos (número, si es VIP, disponibilidad) y
    los comportamientos (reservar, liberar, verificar disponibilidad) relacionados con una mesa.
    Su estado interno (self.disponibilidad) es gestionado a través de sus métodos públicos.
    """

    def __init__(self, numero, es_vip=False):
        """
        Constructor de la clase Mesa.
        Se llama automáticamente cuando se crea una nueva instancia/objeto de Mesa.

        Args:
            numero (int): El número identificador único de la mesa.
            es_vip (bool): True si la mesa es VIP, False en caso contrario. Por defecto es False.
        """
        self.numero = numero
        # Atributo público: Almacena el número de la mesa.
        self.es_vip = es_vip
        # Atributo público: Almacena si la mesa es VIP.
        self.disponibilidad = {}
        # Atributo que gestiona la disponibilidad de la mesa.
        # Es un diccionario donde:
        # - La clave externa es la fecha (string en formato 'YYYY-MM-DD').
        # - El valor es otro diccionario: {hora (int): True/False (disponible/reservado)}.
        # Ejemplo: {'2025-07-03': {13: True, 14: False, 15: True, 16: True}}
        # El acceso y modificación de este atributo están controlados por los métodos de esta clase,
        # lo que es clave para el encapsulamiento.

    def __str__(self):
        """
        Método especial que define la representación en cadena del objeto Mesa.
        Se llama automáticamente cuando se usa print() con un objeto Mesa.
        """
        estado_vip = " (VIP)" if self.es_vip else ""
        return f"Mesa {self.numero}{estado_vip}"
        # Devuelve una cadena legible para identificar la mesa (ej., "Mesa 1", "Mesa 6 (VIP)").

    def inicializar_dia(self, fecha_str, horario_inicio, horario_fin):
        """
        Método público: Inicializa la disponibilidad de la mesa para un día específico.
        Si la fecha no ha sido gestionada antes, se crea y se marcan todas las horas
        dentro del horario de trabajo como disponibles.

        Args:
            fecha_str (str): La fecha a inicializar (formato 'YYYY-MM-DD').
            horario_inicio (int): La primera hora de inicio de reserva (ej., 13).
            horario_fin (int): La última hora de inicio de reserva (ej., 16).
        """
        if fecha_str not in self.disponibilidad:
            # Si la fecha no está en el diccionario de disponibilidad de la mesa...
            # Se crean entradas para todas las horas dentro del rango definido por el restaurante.
            self.disponibilidad[fecha_str] = {hora: True for hora in range(horario_inicio, horario_fin + 1)}
            # Todas las horas se establecen inicialmente como True (disponible).

    def reservar_hora(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Método público: Intenta marcar una hora específica como reservada para esta mesa en una fecha dada.
        Encapsulamiento: Este método es la interfaz controlada para cambiar el estado de disponibilidad de la mesa.
        Maneja la lógica interna de cómo se actualiza la disponibilidad.

        Args:
            fecha_str (str): La fecha de la reserva (formato 'YYYY-MM-DD').
            hora (int): La hora de inicio de la reserva (ej., 13 para 13:00-14:00).
            horario_inicio (int): La primera hora de inicio de reserva.
            horario_fin (int): La última hora de inicio de reserva.

        Returns:
            bool: True si la reserva fue exitosa (la hora estaba disponible), False en caso contrario.
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        # Asegura que el día esté configurado en el diccionario de disponibilidad de la mesa.

        # Verifica si la hora está dentro de las horas gestionadas y si está actualmente disponible.
        if hora in self.disponibilidad[fecha_str] and self.disponibilidad[fecha_str][hora]:
            self.disponibilidad[fecha_str][hora] = False  # Marca la hora como reservada (False).
            return True  # Indica éxito.
        return False  # Indica que la hora no estaba disponible o es inválida.

    def liberar_hora(self, fecha_str, hora):
        """
        Método público: Marca una hora previamente reservada como disponible para esta mesa.
        Encapsulamiento: La forma controlada de "deshacer" una reserva en el estado interno de la mesa.

        Args:
            fecha_str (str): La fecha de la reserva a liberar.
            hora (int): La hora de la reserva a liberar.

        Returns:
            bool: True si la hora se liberó exitosamente, False si no se encontró la reserva.
        """
        if fecha_str in self.disponibilidad and hora in self.disponibilidad[fecha_str]:
            # Verifica si la fecha y la hora existen en los registros de disponibilidad.
            self.disponibilidad[fecha_str][hora] = True  # Marca la hora como disponible (True).
            return True  # Indica éxito.
        return False  # Indica que la fecha o la hora no se encontraron para liberar.

    def esta_disponible(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Método público: Verifica si la mesa está disponible en una hora y fecha específicas.
        Encapsulamiento: La interfaz para consultar el estado interno de la mesa sin modificarlo.

        Args:
            fecha_str (str): La fecha a consultar.
            hora (int): La hora a consultar.
            horario_inicio (int): La primera hora de inicio de reserva.
            horario_fin (int): La última hora de inicio de reserva.

        Returns:
            bool: True si la mesa está disponible en esa hora y fecha, False en caso contrario.
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        # Asegura que el día esté inicializado para poder consultar su disponibilidad.
        # Utiliza .get() para acceder de forma segura a los diccionarios anidados.
        # Si la fecha o la hora no existen, .get() devuelve el valor por defecto (False),
        # lo que significa que la mesa no está disponible.
        return self.disponibilidad.get(fecha_str, {}).get(hora, False)


class Reserva:
    """
    Clase Reserva: Representa una reservación hecha por un cliente.
    Encapsulamiento: Agrupa todos los detalles de una reserva (cliente, fecha, hora, mesa, folio)
    y la lógica para generar su folio. Los datos de la reserva se mantienen juntos.
    """

    def __init__(self, cliente_nombre, fecha_str, hora, mesa):
        """
        Constructor de la clase Reserva.

        Args:
            cliente_nombre (str): Nombre del cliente que realiza la reserva.
            fecha_str (str): La fecha de la reserva (formato 'YYYY-MM-DD').
            hora (int): La hora de inicio de la reserva.
            mesa (Mesa): El objeto Mesa que ha sido reservado. (Asociación: una Reserva "tiene una" Mesa).
        """
        self.cliente_nombre = cliente_nombre
        # Atributo público: Nombre del cliente.
        self.fecha_str = fecha_str
        # Atributo público: Fecha de la reserva.
        self.hora = hora
        # Atributo público: Hora de la reserva.
        self.mesa = mesa
        # Atributo público: Referencia al objeto Mesa asociado a esta reserva.
        self.folio = self._generar_folio()
        # Atributo público: Folio único de la reserva, generado automáticamente.

    def _generar_folio(self):
        """
        Método "protegido" (por convención, debido al prefijo '_').
        Encapsulamiento: Este método está diseñado para ser utilizado internamente
        por el constructor de la clase para asegurar que el folio se genere
        de manera consistente y controlada. No se espera que se llame directamente
        desde fuera de un objeto Reserva.
        """
        prefijo = "VX" if self.mesa.es_vip else "GX"
        # Determina el prefijo del folio: 'VX' para VIP, 'GX' para General.
        return f"{prefijo}{self.mesa.numero}"
        # Retorna el folio combinando el prefijo y el número de la mesa.

    def __str__(self):
        """
        Método especial para la representación en cadena del objeto Reserva.
        """
        return (f"Reserva para {self.cliente_nombre} "
                f"en {self.mesa} el {self.fecha_str} a las {self.hora}:00. Folio: {self.folio}")


class Restaurante:
    """
    Clase Restaurante: Actúa como el sistema principal de gestión de reservas.
    Clase Controladora: Coordina las interacciones entre los objetos Mesa y Reserva.
    Encapsulamiento: Encapsula la colección de todas las mesas y reservas,
    y proporciona los métodos públicos que corresponden a los casos de uso
    (la interfaz del sistema para el "Empleado").
    La lógica interna de cómo se gestionan las colecciones o las validaciones está oculta.
    """

    def __init__(self):
        """
        Constructor de la clase Restaurante.
        Inicializa la lista de mesas (5 generales, 5 VIP) y la lista de reservas.
        Define el horario de operación para las reservas.
        """
        self.mesas = []
        # Lista para almacenar todos los objetos Mesa del restaurante.

        # Creación de 5 mesas en zona general (numeradas del 1 al 5).
        for i in range(1, 6):
            self.mesas.append(Mesa(i, es_vip=False))

        # Creación de 5 mesas VIP (numeradas del 6 al 10).
        # Se les asigna un número de mesa a partir del 6 para distinguirlas.
        for i in range(1, 6):
            self.mesas.append(Mesa(5 + i, es_vip=True))

        self.reservas = []
        # Lista para almacenar todos los objetos Reserva creados en el sistema.

        self.horario_inicio = 13  # La primera hora de inicio de reserva (13:00 para 13:00-14:00).
        self.horario_fin = 16     # La última hora de inicio de reserva (16:00 para 16:00-17:00).
                                  # Esto define las 4 franjas de una hora.

    def _validar_hora(self, hora):
        """
        Método "protegido": Valida si una hora dada está dentro del horario de reservas del restaurante.
        Encapsulamiento: Es un método auxiliar interno, no parte de la interfaz pública del sistema.
        La lógica de validación de horarios está encapsulada aquí.
        """
        return self.horario_inicio <= hora <= self.horario_fin

    def _validar_fecha(self, fecha_str):
        """
        Método "protegido": Valida si una cadena de texto tiene el formato de fecha 'YYYY-MM-DD' válido.
        Encapsulamiento: Otro método auxiliar interno para la validación de entrada.
        """
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def ver_disponibilidad(self, fecha_str):
        """
        Método público: Implementa el Caso de Uso "Ver disponibilidad".
        Permite al empleado visualizar la disponibilidad de mesas para un día específico.
        Encapsulamiento: Oculta la complejidad de iterar sobre mesas y sus estados internos.
        """
        # Precondición: El formato de la fecha debe ser válido.
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return

        print(f"\n--- Disponibilidad para el {fecha_str} ---")
        disponibilidad_encontrada = False # Bandera para saber si se mostró algo.

        # Itera sobre todas las mesas, ordenándolas: VIP primero, luego por número.
        for mesa in sorted(self.mesas, key=lambda m: (not m.es_vip, m.numero)):
            # Asegura que el día esté inicializado para cada mesa antes de mostrar su disponibilidad.
            mesa.inicializar_dia(fecha_str, self.horario_inicio, self.horario_fin)
            print(f"\n{mesa}:")
            horas_disponibles_mesa = []
            # Itera sobre las horas del horario de reservas para cada mesa.
            for hora in range(self.horario_inicio, self.horario_fin + 1):
                # Utiliza el método encapsulado de la clase Mesa para verificar su estado.
                estado = "Disponible" if mesa.esta_disponible(fecha_str, hora, self.horario_inicio, self.horario_fin) else "Reservado"
                # Formatea la salida para mostrar los intervalos de una hora.
                horas_disponibles_mesa.append(f" {hora}:00-{hora+1}:00 -> {estado}")
                disponibilidad_encontrada = True # Marca que se encontró disponibilidad.
            print("".join(horas_disponibles_mesa))

        if not disponibilidad_encontrada:
            print("No hay información de disponibilidad para las mesas en esta fecha.")
        print("---------------------------------")

    def hacer_reservacion(self, cliente_nombre, fecha_str, hora, numero_mesa):
        """
        Método público: Implementa el Caso de Uso "Hacer reservación".
        Permite al empleado generar una nueva reservación.
        Encapsulamiento: Proporciona una interfaz para crear reservas, ocultando
        toda la lógica de validación, búsqueda de mesa, y actualización de estados.
        """
        # Precondición: Los campos requeridos deben estar completos.
        if not all([cliente_nombre, fecha_str, hora, numero_mesa]):
            print("❌ Error: La reservación no se guarda porque faltan datos. Por favor, complete todos los campos.")
            return None

        # Proceso Alternativo / Situaciones de Error: Validación de fecha y hora.
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return None
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario de reservas es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return None

        # Búsqueda de la mesa seleccionada.
        mesa_seleccionada = None
        for mesa in self.mesas:
            if mesa.numero == numero_mesa:
                mesa_seleccionada = mesa
                break

        # Situación de Error: Mesa no encontrada.
        if not mesa_seleccionada:
            print(f"❌ Error: Mesa {numero_mesa} no encontrada.")
            return None

        # Situación de Error: Mesa no disponible en la hora/fecha.
        # Utiliza el método encapsulado de Mesa para verificar disponibilidad.
        if not mesa_seleccionada.esta_disponible(fecha_str, hora, self.horario_inicio, self.horario_fin):
            print(f"❌ Error: La mesa {numero_mesa} no está disponible el {fecha_str} a las {hora}:00.")
            return None

        # Proceso Estándar: Si todas las validaciones son exitosas.
        # Utiliza el método encapsulado de Mesa para marcar la hora como reservada.
        if mesa_seleccionada.reservar_hora(fecha_str, hora, self.horario_inicio, self.horario_fin):
            nueva_reserva = Reserva(cliente_nombre, fecha_str, hora, mesa_seleccionada)
            self.reservas.append(nueva_reserva) # Agrega la nueva reserva a la lista del sistema.
            # Postcondición: La reservación ha quedado guardada en el sistema.
            print(f"✅ ¡Reservación exitosa! {nueva_reserva}")
            return nueva_reserva
        else:
            # Error inesperado si reservar_hora retorna False a pesar de las verificaciones previas.
            print("❌ Error inesperado al intentar reservar la mesa.")
            return None

    def eliminar_reservacion(self, fecha_str, hora, folio_mesa):
        """
        Método público: Implementa el Caso de Uso "Eliminar reservación".
        Permite al empleado eliminar una reservación existente.
        Encapsulamiento: Centraliza la lógica de búsqueda, confirmación y eliminación de una reserva,
        así como la actualización del estado de la mesa.
        """
        # Precondición: Los datos para identificar la reserva deben estar presentes.
        if not all([fecha_str, hora, folio_mesa]):
            print("❌ Error: Por favor, complete todos los datos para eliminar la reserva.")
            return False

        # Proceso Alternativo / Situaciones de Error: Validación de fecha y hora.
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return False
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario de reservas es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return False

        # Búsqueda de la reserva a eliminar.
        reserva_encontrada = None
        for reserva in self.reservas:
            # Comparamos folio, fecha y hora para asegurar que es la reserva correcta.
            if (reserva.folio == folio_mesa and
                reserva.fecha_str == fecha_str and
                reserva.hora == hora):
                reserva_encontrada = reserva
                break

        # Situación de Error: Reserva no encontrada.
        if not reserva_encontrada:
            print(f"❌ Error: No se encontró una reservación con el folio '{folio_mesa}' "
                  f"para el {fecha_str} a las {hora}:00.")
            return False

        # Paso de Confirmación (simulado, según tus descripciones).
        confirmacion = input(f"¿Está seguro que desea eliminar la reserva de {reserva_encontrada.cliente_nombre} "
                             f"para la mesa {reserva_encontrada.mesa.numero} el {reserva_encontrada.fecha_str} a las {reserva_encontrada.hora}:00? (s/n): ").lower()
        if confirmacion != 's':
            print("🚫 Eliminación cancelada.")
            return False

        # Proceso Estándar: Si se confirma.
        self.reservas.remove(reserva_encontrada) # Elimina el objeto Reserva de la lista del sistema.
        # Postcondición: Se ha eliminado la reservación.

        # Actualiza la disponibilidad de la mesa utilizando el método encapsulado de Mesa.
        reserva_encontrada.mesa.liberar_hora(fecha_str, hora)
        # Postcondición: El sistema muestra la mesa como "disponible" en "Ver disponibilidad".
        print(f"✅ Reservación para '{reserva_encontrada.cliente_nombre}' eliminada exitosamente.")
        return True

# --- Simulación de la interacción del Empleado (Programa Principal) ---

def mostrar_menu():
    """
    Función auxiliar: Muestra las opciones disponibles para el Empleado.
    No es parte de ninguna clase, actúa como la "interfaz" de consola.
    """
    print("\n--- Menú del Sistema de Reservas ---")
    print("1. Ver Disponibilidad")
    print("2. Hacer Reservación")
    print("3. Eliminar Reservación")
    print("4. Salir")
    print("-----------------------------------")

if __name__ == "__main__":
    # Este bloque se ejecuta solo cuando el script se inicia directamente,
    # no cuando se importa como un módulo en otro archivo.
    # Es el punto de entrada de nuestro programa.

    restaurante = Restaurante() # Crea una instancia de nuestro sistema de reservas.

    while True:
        # Bucle principal del programa: Mantiene la aplicación en ejecución
        # y permite al usuario interactuar repetidamente.
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Ejecuta el Caso de Uso "Ver Disponibilidad".
            fecha_disp = input("Ingrese la fecha para ver disponibilidad (YYYY-MM-DD): ")
            restaurante.ver_disponibilidad(fecha_disp)
            # Llama al método público de la clase Restaurante.

        elif opcion == '2':
            # Ejecuta el Caso de Uso "Hacer Reservación".
            print("\n--- Hacer Reservación ---")
            cliente_nombre = input("Nombre del cliente: ")
            fecha_reserva = input("Fecha de la reserva (YYYY-MM-DD): ")
            try:
                # Se utiliza try-except para manejar errores si el usuario no ingresa un número entero.
                hora_reserva = int(input(f"Hora de la reserva ({restaurante.horario_inicio}-{restaurante.horario_fin}): "))
            except ValueError:
                print("❌ Hora inválida. Debe ser un número entero.")
                continue # Vuelve al inicio del bucle para mostrar el menú de nuevo.
            try:
                numero_mesa = int(input("Número de mesa deseada: "))
            except ValueError:
                print("❌ Número de mesa inválido. Debe ser un número entero.")
                continue # Vuelve al inicio del bucle.

            restaurante.hacer_reservacion(cliente_nombre, fecha_reserva, hora_reserva, numero_mesa)
            # Llama al método público de la clase Restaurante.

        elif opcion == '3':
            # Ejecuta el Caso de Uso "Eliminar Reservación".
            print("\n--- Eliminar Reservación ---")
            folio_eliminar = input("Folio de la reserva a eliminar (ej. VX1, GX2): ")
            fecha_eliminar = input("Fecha de la reserva (YYYY-MM-DD): ")
            try:
                hora_eliminar = int(input(f"Hora de la reserva ({restaurante.horario_inicio}-{restaurante.horario_fin}): "))
            except ValueError:
                print("❌ Hora inválida. Debe ser un número entero.")
                continue

            restaurante.eliminar_reservacion(fecha_eliminar, hora_eliminar, folio_eliminar)
            # Llama al método público de la clase Restaurante. La lógica de búsqueda
            # y validación de la reserva está encapsulada dentro de este método.

        elif opcion == '4':
            # Opción para salir del programa.
            print("Saliendo del sistema. ¡Hasta luego!")
            break # Rompe el bucle 'while True', terminando la ejecución del programa.

        else:
            # Manejo de opción no válida.
            print("Opción no válida. Por favor, intente de nuevo.")
