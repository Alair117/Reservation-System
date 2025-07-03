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

# Importa el módulo datetime para manejar fechas y horas.

# --- CLASES ---

class MesaBase:
    """
    Clase Base para representar cualquier tipo de mesa en el restaurante.
    Encapsulamiento: Agrupa los datos fundamentales de una mesa (número, disponibilidad) y
    los comportamientos básicos de gestión de su estado de disponibilidad.
    """

    def __init__(self, numero):
        """
        Constructor de la clase MesaBase.
        Args:
            numero (int): El número identificador único de la mesa.
        """
        self.numero = numero
        self.disponibilidad = {} # Gestionado internamente.

    def __str__(self):
        """
        Método especial para la representación en cadena.
        Este será sobrescrito por las clases hijas para añadir especificidad.
        """
        return f"Mesa {self.numero}"

    def inicializar_dia(self, fecha_str, horario_inicio, horario_fin):
        """
        Método público: Inicializa la disponibilidad para un día específico.
        """
        if fecha_str not in self.disponibilidad:
            self.disponibilidad[fecha_str] = {hora: True for hora in range(horario_inicio, horario_fin + 1)}

    def reservar_hora(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Método público: Intenta marcar una hora como reservada.
        Encapsulamiento: Controla cómo se modifica el estado de disponibilidad.
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        if hora in self.disponibilidad[fecha_str] and self.disponibilidad[fecha_str][hora]:
            self.disponibilidad[fecha_str][hora] = False
            return True
        return False

    def liberar_hora(self, fecha_str, hora):
        """
        Método público: Libera una hora previamente reservada.
        Encapsulamiento: Controla cómo se modifica el estado de disponibilidad.
        """
        if fecha_str in self.disponibilidad and hora in self.disponibilidad[fecha_str]:
            self.disponibilidad[fecha_str][hora] = True
            return True
        return False

    def esta_disponible(self, fecha_str, hora, horario_inicio, horario_fin):
        """
        Método público: Consulta la disponibilidad de la mesa.
        Encapsulamiento: Controla cómo se accede al estado de disponibilidad.
        """
        self.inicializar_dia(fecha_str, horario_inicio, horario_fin)
        return self.disponibilidad.get(fecha_str, {}).get(hora, False)

    # Nuevo método para obtener si es VIP, útil para el folio de reserva
    # Esto es un "getter" básico para un atributo.
    def es_vip_mesa(self):
        """Método abstracto que las subclases deben implementar."""
        raise NotImplementedError("Las subclases deben implementar este método para indicar si son VIP.")


class MesaGeneral(MesaBase):
    """
    Clase hija: Representa una mesa de la zona general.
    Herencia: Hereda de MesaBase.
    Polimorfismo: Sobreescribe __str__ para su representación específica.
    """
    def __init__(self, numero):
        super().__init__(numero) # Llama al constructor de la clase padre.

    def __str__(self):
        return f"Mesa {self.numero} (General)" # Representación específica para mesas generales.

    def es_vip_mesa(self):
        return False


class MesaVIP(MesaBase):
    """
    Clase hija: Representa una mesa de la zona VIP.
    Herencia: Hereda de MesaBase.
    Polimorfismo: Sobreescribe __str__ para su representación específica.
    """
    def __init__(self, numero):
        super().__init__(numero) # Llama al constructor de la clase padre.

    def __str__(self):
        return f"Mesa {self.numero} (VIP)" # Representación específica para mesas VIP.

    def es_vip_mesa(self):
        return True


class Reserva:
    """
    Clase Reserva: Representa una reservación.
    Encapsulamiento: Agrupa los detalles de la reserva y la lógica de folio.
    """
    def __init__(self, cliente_nombre, fecha_str, hora, mesa):
        self.cliente_nombre = cliente_nombre
        self.fecha_str = fecha_str
        self.hora = hora
        self.mesa = mesa # Referencia al objeto Mesa (MesaGeneral o MesaVIP).
        self.folio = self._generar_folio() # Genera folio usando el método interno.

    def _generar_folio(self):
        """
        Método "protegido": Genera el folio de la reserva.
        Encapsulamiento: Lógica interna para la generación del folio.
        Polimorfismo (implícito): Usa el método es_vip_mesa() de la mesa,
        que se comporta diferente si la mesa es MesaVIP o MesaGeneral.
        """
        prefijo = "VX" if self.mesa.es_vip_mesa() else "GX"
        return f"{prefijo}{self.mesa.numero}"

    def __str__(self):
        """
        Método especial para la representación en cadena del objeto Reserva.
        """
        return (f"Reserva para {self.cliente_nombre} "
                f"en {self.mesa} el {self.fecha_str} a las {self.hora}:00. Folio: {self.folio}")


class Restaurante:
    """
    Clase Restaurante: Gestiona mesas y reservaciones.
    Clase Controladora: Coordina las interacciones.
    Encapsulamiento: Oculta las colecciones de mesas y reservas y su gestión interna.
    Abstracción: Los métodos de caso de uso (ver_disponibilidad, hacer_reservacion, eliminar_reservacion)
                 ocultan la complejidad subyacente.
    """

    def __init__(self):
        """
        Constructor de la clase Restaurante.
        Inicializa la lista de mesas (usando las clases hijas) y la lista de reservas.
        """
        self.mesas = []
        # Crea 5 mesas generales (numeradas del 1 al 5)
        for i in range(1, 6):
            self.mesas.append(MesaGeneral(i)) # Instancia de MesaGeneral
        # Crea 5 mesas VIP (numeradas del 6 al 10)
        for i in range(1, 6):
            self.mesas.append(MesaVIP(5 + i)) # Instancia de MesaVIP

        self.reservas = []
        self.horario_inicio = 13
        self.horario_fin = 16

    def _validar_hora(self, hora):
        """
        Método "protegido": Valida si una hora está dentro del horario.
        Encapsulamiento: Lógica auxiliar interna.
        """
        return self.horario_inicio <= hora <= self.horario_fin

    def _validar_fecha(self, fecha_str):
        """
        Método "protegido": Valida el formato de la fecha.
        Encapsulamiento: Lógica auxiliar interna.
        """
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def ver_disponibilidad(self, fecha_str):
        """
        Caso de Uso: Ver disponibilidad.
        Polimorfismo: Itera sobre objetos MesaBase (que pueden ser MesaGeneral o MesaVIP)
                      y llama a sus métodos, como __str__ y esta_disponible, que se comportan
                      de forma polimórfica según el tipo real del objeto.
        """
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. UsebeginPath-MM-DD.")
            return

        print(f"\n--- Disponibilidad para el {fecha_str} ---")
        disponibilidad_encontrada = False

        # El ordenamiento se hace por si es VIP y luego por número de mesa
        for mesa in sorted(self.mesas, key=lambda m: (not m.es_vip_mesa(), m.numero)):
            mesa.inicializar_dia(fecha_str, self.horario_inicio, self.horario_fin)
            # Polimorfismo: Aquí, `mesa.__str__()` se llamará automáticamente,
            # lo que significa que se ejecutará el __str__ de MesaGeneral o MesaVIP.
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
        """
        Caso de Uso: Hacer reservación.
        Polimorfismo: Se interactúa con la `mesa_seleccionada` (que es de tipo MesaBase)
                      llamando a `mesa_seleccionada.esta_disponible()` y `mesa_seleccionada.reservar_hora()`.
                      Estos métodos operan de la misma manera, sin importar si la mesa es General o VIP,
                      demostrando la uniformidad de la interfaz.
        """
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
        for mesa in self.mesas: # Iterando sobre objetos de tipo MesaBase
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
        """
        Caso de Uso: Eliminar reservación.
        Polimorfismo: Al liberar la mesa (`reserva_encontrada.mesa.liberar_hora()`),
                      el método `liberar_hora` se comporta igual para cualquier tipo de Mesa,
                      porque está implementado en la clase base.
        """
        if not all([fecha_str, hora, folio_mesa]):
            print("❌ Error: Por favor, complete todos los datos para eliminar la reserva.")
            return False

        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. UsebeginPath-MM-DD.")
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

# --- SIMULACIÓN DE INTERACCIÓN DEL EMPLEADO ---

def mostrar_menu():
    """
    Función auxiliar: Muestra las opciones disponibles para el Empleado.
    """
    print("\n--- Menú del Sistema de Reservas ---")
    print("1. Ver Disponibilidad")
    print("2. Hacer Reservación")
    print("3. Eliminar Reservación")
    print("4. Salir")
    print("-----------------------------------")

if __name__ == "__main__":
    restaurante = Restaurante() # Instancia del sistema de reservas.

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
