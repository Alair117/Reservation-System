import datetime

class Mesa:
    """Representa una mesa en el restaurante."""
    def __init__(self, numero, es_vip=False):
        self.numero = numero
        self.es_vip = es_vip
        # La disponibilidad se gestiona por hora para un día específico
        # Usaremos un diccionario donde la clave es la fecha (YYYY-MM-DD)
        # y el valor es otro diccionario para las horas {HH: True/False (disponible/reservado)}
        self.disponibilidad = {}

    def __str__(self):
        estado_vip = " (VIP)" if self.es_vip else ""
        return f"Mesa {self.numero}{estado_vip}"

    def inicializar_dia(self, fecha_str):
        """Inicializa la disponibilidad para un día dado."""
        if fecha_str not in self.disponibilidad:
            # Horario de 13:00 a 17:00
            self.disponibilidad[fecha_str] = {hora: True for hora in range(13, 18)} # 13, 14, 15, 16, 17

    def reservar_hora(self, fecha_str, hora):
        """Marca una hora como reservada para una fecha específica."""
        self.inicializar_dia(fecha_str) # Asegura que el día esté inicializado
        if hora in self.disponibilidad[fecha_str] and self.disponibilidad[fecha_str][hora]:
            self.disponibilidad[fecha_str][hora] = False
            return True
        return False # No disponible o fuera de horario

    def liberar_hora(self, fecha_str, hora):
        """Marca una hora como disponible para una fecha específica."""
        if fecha_str in self.disponibilidad and hora in self.disponibilidad[fecha_str]:
            self.disponibilidad[fecha_str][hora] = True
            return True
        return False # No se encontró la hora para liberar

    def esta_disponible(self, fecha_str, hora):
        """Verifica si la mesa está disponible en una hora y fecha específicas."""
        self.inicializar_dia(fecha_str) # Asegura que el día esté inicializado
        return self.disponibilidad.get(fecha_str, {}).get(hora, False) # Retorna False si no existe la hora o fecha


class Reserva:
    """Representa una reservación."""
    def __init__(self, cliente_nombre, fecha_str, hora, mesa):
        self.cliente_nombre = cliente_nombre
        self.fecha_str = fecha_str
        self.hora = hora
        self.mesa = mesa
        self.folio = self._generar_folio() # Genera un folio al crear la reserva

    def _generar_folio(self):
        # VX para VIP, GX para General. X es el número de la mesa.
        prefijo = "VX" if self.mesa.es_vip else "GX"
        return f"{prefijo}{self.mesa.numero}"

    def __str__(self):
        return (f"Reserva para {self.cliente_nombre} "
                f"en {self.mesa} el {self.fecha_str} a las {self.hora}:00. Folio: {self.folio}")

class Restaurante:
    """Gestiona las mesas y las reservaciones del restaurante."""
    def __init__(self, num_mesas_normales=5, num_mesas_vip=2):
        self.mesas = []
        for i in range(1, num_mesas_normales + 1):
            self.mesas.append(Mesa(i))
        for i in range(1, num_mesas_vip + 1):
            self.mesas.append(Mesa(num_mesas_normales + i, es_vip=True))
        self.reservas = []
        self.horario_inicio = 13
        self.horario_fin = 17 # Hasta las 17:00, por lo que el rango es hasta 17

    def _validar_hora(self, hora):
        return self.horario_inicio <= hora <= self.horario_fin

    def _validar_fecha(self, fecha_str):
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def ver_disponibilidad(self, fecha_str):
        """
        Caso de Uso: Ver disponibilidad
        Permite al empleado visualizar la disponibilidad de mesas para un día específico.
        """
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return

        print(f"\n--- Disponibilidad para el {fecha_str} ---")
        disponibilidad_encontrada = False
        for mesa in sorted(self.mesas, key=lambda m: (not m.es_vip, m.numero)): # VIP primero
            mesa.inicializar_dia(fecha_str) # Asegura que el día esté inicializado para todas las mesas
            print(f"\n{mesa}:")
            horas_disponibles_mesa = []
            for hora in range(self.horario_inicio, self.horario_fin + 1):
                estado = "Disponible" if mesa.esta_disponible(fecha_str, hora) else "Reservado"
                horas_disponibles_mesa.append(f" {hora}:00 -> {estado}")
                disponibilidad_encontrada = True
            print("".join(horas_disponibles_mesa))

        if not disponibilidad_encontrada:
            print("No hay información de disponibilidad para las mesas en esta fecha.")
        print("---------------------------------")


    def hacer_reservacion(self, cliente_nombre, fecha_str, hora, numero_mesa):
        """
        Caso de Uso: Hacer reservación
        Permite al empleado generar una reservación.
        """
        # Precondición: Campos requeridos
        if not all([cliente_nombre, fecha_str, hora, numero_mesa]):
            print("❌ Error: La reservación no se guarda porque faltan datos. Por favor, complete todos los campos.")
            return None

        # Validación de fecha y hora
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return None
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario laboral es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return None

        mesa_seleccionada = None
        for mesa in self.mesas:
            if mesa.numero == numero_mesa:
                mesa_seleccionada = mesa
                break

        if not mesa_seleccionada:
            print(f"❌ Error: Mesa {numero_mesa} no encontrada.")
            return None

        if not mesa_seleccionada.esta_disponible(fecha_str, hora):
            print(f"❌ Error: La mesa {numero_mesa} no está disponible el {fecha_str} a las {hora}:00.")
            return None

        # Proceso estándar: Reservar la mesa
        if mesa_seleccionada.reservar_hora(fecha_str, hora):
            nueva_reserva = Reserva(cliente_nombre, fecha_str, hora, mesa_seleccionada)
            self.reservas.append(nueva_reserva)
            print(f"✅ ¡Reservación exitosa! {nueva_reserva}")
            return nueva_reserva
        else:
            print("❌ Error inesperado al intentar reservar la mesa.")
            return None

    def eliminar_reservacion(self, fecha_str, hora, folio_mesa):
        """
        Caso de Uso: Eliminar reservación
        Permite al empleado eliminar una reservación.
        """
        # Precondición: Campos requeridos (aunque tus tablas no lo indican explícitamente para error, es buena práctica)
        if not all([fecha_str, hora, folio_mesa]):
            print("❌ Error: Por favor, complete todos los datos para eliminar la reserva.")
            return False

        # Validación de fecha y hora
        if not self._validar_fecha(fecha_str):
            print("❌ Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return False
        if not self._validar_hora(hora):
            print(f"❌ Error: Hora inválida. El horario laboral es de {self.horario_inicio}:00 a {self.horario_fin}:00.")
            return False

        reserva_encontrada = None
        for reserva in self.reservas:
            # Comparamos folio, fecha y hora para asegurar que es la reserva correcta
            if (reserva.folio == folio_mesa and
                reserva.fecha_str == fecha_str and
                reserva.hora == hora):
                reserva_encontrada = reserva
                break

        if not reserva_encontrada:
            print(f"❌ Error: No se encontró una reservación con el folio '{folio_mesa}' "
                  f"para el {fecha_str} a las {hora}:00.")
            return False

        # Confirmación (simulada)
        confirmacion = input(f"¿Está seguro que desea eliminar la reserva de {reserva_encontrada.cliente_nombre} "
                             f"para la mesa {reserva_encontrada.mesa.numero} el {fecha_encontrada} a las {hora_encontrada}:00? (s/n): ").lower()
        if confirmacion != 's':
            print("🚫 Eliminación cancelada.")
            return False

        # Proceso estándar: Eliminar la reserva y liberar la mesa
        self.reservas.remove(reserva_encontrada)
        reserva_encontrada.mesa.liberar_hora(fecha_str, hora)
        print(f"✅ Reservación para '{reserva_encontrada.cliente_nombre}' eliminada exitosamente.")
        # La postcondición indica "el sistema muestra la mesa como 'disponible' en la opción del menú 'Ver Disponibilidad'"
        # Esto ya lo maneja Mesa.liberar_hora y se reflejaría en la próxima llamada a ver_disponibilidad.
        return True

# --- Simulación de la interacción del Empleado (Main Program) ---

def mostrar_menu():
    print("\n--- Menú del Sistema de Reservas ---")
    print("1. Ver Disponibilidad")
    print("2. Hacer Reservación")
    print("3. Eliminar Reservación")
    print("4. Salir")
    print("-----------------------------------")

if __name__ == "__main__":
    restaurante = Restaurante(num_mesas_normales=3, num_mesas_vip=1) # Por ejemplo, 3 mesas normales y 1 VIP

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

            # Buscar la reserva para obtener los datos exactos que se requieren para confirmar al usuario
            reserva_a_eliminar = None
            for r in restaurante.reservas:
                if r.folio == folio_eliminar and r.fecha_str == fecha_eliminar and r.hora == hora_eliminar:
                    reserva_a_eliminar = r
                    break

            if reserva_a_eliminar:
                # Se pasa la información que se necesita para encontrarla, no el objeto entero
                restaurante.eliminar_reservacion(fecha_eliminar, hora_eliminar, folio_eliminar)
            else:
                print(f"❌ Error: No se encontró una reserva con el folio '{folio_eliminar}' para el {fecha_eliminar} a las {hora_eliminar}:00.")

        elif opcion == '4':
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")