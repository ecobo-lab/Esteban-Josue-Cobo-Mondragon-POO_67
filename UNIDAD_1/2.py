class DispositivoIoT:
    def __init__(self, id_dispositivo, tipo_sensor, estado, nivel_bateria):

        self.id_dispositivo=id_dispositivo
        self.tipo_sensor=tipo_sensor
        self.estado=estado
        self.nivel_bateria=nivel_bateria

    def conectar_red():
        pass
    def enviar_datos():
        pass
    def recibir_comando():
        pass
    def mostrar_estado():
        pass
IoT= DispositivoIoT("TERM-HOGAR-01","Temperatura y Humedad","Conectado","95%")
print(IoT.id_dispositivo)