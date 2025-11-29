class Robot1:
    def __init__(self,nombre,tipo,tarea):
        self.nombre=nombre
        self.tipo=tipo
        self.tarea=tarea
    def mover():
        pass
    def atras():
        pass
    def giro_iz():
        pass
    def giro_der():
        pass
titanus= Robot1("Titanus","batalla","atacar")
print(titanus.nombre)


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

class Robot:
    def __init__(self, nombre, modelo, nivel_energia, tarea_actual):
    
        self.nombre = nombre
        self.modelo = modelo
        self.nivel_energia = nivel_energia
        self.tarea_actual = tarea_actual

    def moverse():
        pass
    def realizar_tarea():
        pass
    def recargar():
        pass
    def hablar():
        pass
Robby= Robot("Robby","ClanBot","55%","Limpiando sala de estar")
print(Robby.nombre)

class Navegador:
    def __init__(self, nombre, version, historial, pestanas_abiertas):
        
        self.nombre = nombre
        self.version = version
        self.historial = historial
        self.pestanas_abiertas = pestanas_abiertas

    def abrir_pagina():
        pass
    def cerrar_pestana():
        pass
    def actualizar_pagina():
        pass
    def limpiar_historial():
        pass
Mozilla= Navegador("Mozilla Firefox","125.0.3","Lista de 500 URLs visitadas","Youtube-Wikipedia-Gmail")
print(Mozilla.nombre)

class ComputadorPC:
    def __init__(self, marca, procesador, memoria_ram, almacenamiento):
       
        self.marca = marca
        self.procesador = procesador
        self.memoria_ram = memoria_ram
        self.almacenamiento = almacenamiento

    def encender():
        pass
    def apagar():
        pass
    def ejecutar_programa():
        pass
    def mostrar_informacion():
        pass
HP= ComputadorPC("HP","Intel core I5 13va Gen","16GB","1TB SSD")
print(HP.marca)

class Telefono:
    def __init__(self, marca, numero_telefono, nivel_bateria, sistema_operativo):
        
        self.marca = marca
        self.numero_telefono = numero_telefono
        self.nivel_bateria = nivel_bateria
        self.sistema_operativo = sistema_operativo

    def llamar():
        pass
    def enviar_mensaje():
        pass
    def tomar_foto():
        pass
    def abrir_aplicacion():
        pass
Samsung= Telefono("Samsung","0991234567","78%","Android 14")
print(Samsung.marca)

class Arbol:
    def __init__(self, tipo, altura, edad, estado_salud):
       
        self.tipo = tipo
        self.altura = altura
        self.edad = edad
        self.estado_salud = estado_salud

    def crecer():
        pass
    def producir_oxigeno():
        pass
    def absorber_agua():
        pass
    def florecer():
        pass
Pino= Arbol("Pino","15 Metros","45 Años","Saludable")
print(Pino.tipo)

class Cine:
    def __init__(self, nombre, ubicacion, numero_salas, cartelera):

        self.nombre = nombre
        self.ubicacion = ubicacion
        self.numero_salas = numero_salas
        self.cartelera = cartelera

    def proyectar_pelicula():
        pass
    def vender_entrada():
        pass
    def actualizar_cartelera():
        pass
    def limpiar_sala():
        pass
SuperCines= Cine("SuperCines","SuperCines 6 de Diciembre","10","Pelicula1-Pelicula2-Pelicula3...")
print(SuperCines.nombre)

class InteligenciaArtificial:
    def __init__(self, nombre, tipo_modelo, nivel_aprendizaje, version):
    
        self.nombre = nombre
        self.tipo_modelo = tipo_modelo
        self.nivel_aprendizaje = nivel_aprendizaje
        self.version = version

    def entrenar():
        pass
    def predecir():
        pass
    def mejorar_modelo():
        pass
    def responder():
        pass
Gemini= InteligenciaArtificial("Google Gemini","Gemini un modelo lingüístico grande","Training","2.5")
print(Gemini.nombre)

class RedesSociales:
    def __init__(self, nombre, usuarios, publicaciones, servidores_activos):
    
        self.nombre = nombre
        self.usuarios = usuarios
        self.publicaciones = publicaciones
        self.servidores_activos = servidores_activos

    def crear_cuenta():
        pass
    def publicar():
        pass
    def enviar_mensaje():
        pass
    def eliminar_cuenta():
        pass
Ig= RedesSociales("Instagram","Más de 2 billones","Historias, Reels, Fotos","Miles (en data centers de Meta)")
print(Ig.nombre)