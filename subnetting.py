from prettytable import PrettyTable
import time
import os
nameSubred = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S')
class subred:
    def __init__(self, cantidad_de_hosts: int, cantidad_de_puertas_de_enlace: int):
        self.cantidad_de_hosts = cantidad_de_hosts
        self.name = ''
        self.mascara_reducida = ''
        self.mascara_en_decimal = ''
        self.mascara_en_binario = ''
        self.network = ''
        self.network_en_binario = ''
        self.broadcast = ''
        self.broadcast_en_binario = ''
        if cantidad_de_puertas_de_enlace == 1:
            self.cantidad_de_gateways = 1
            self.gateway = ''
            self.gateway_en_binario = ''
        else:
            self.cantidad_de_gateways = cantidad_de_puertas_de_enlace
            self.gateway = []
            self.gateway_en_binario = []
            for i in range(0, cantidad_de_puertas_de_enlace):
                self.gateway.append('')
                self.gateway_en_binario.append('')
        self.rango = ''
        self.cantidad_de_conexiones = self.cantidad_de_hosts + 2 + self.cantidad_de_gateways
        self.bits_necesarios = self.Buscar_bits_necesarios(self.cantidad_de_conexiones)
        self.rango = ''

    def Buscar_bits_necesarios(self, cantidad_de_conexiones: int):
        contador = 1
        for a in range(0, 100):
            if cantidad_de_conexiones <= (2 ** a):
                return contador - 1
            contador += 1

    def __Mostrar__(self, ip: str):
        print(ip)


class subred_interna:
    def __init__(self, router1, router2):
        self.name = router1 + '-' + router2
        self.cantidad_de_hosts = 2
        self.mascara_reducida = ''
        self.mascara_en_decimal = ''
        self.mascara_en_binario = ''
        self.network = ''
        self.network_en_binario = ''
        self.broadcast = ''
        self.broadcast_en_binario = ''
        self.gateway = '---'
        self.cantidad_de_conexiones = self.cantidad_de_hosts + 2
        self.bits_necesarios = self.Buscar_bits_necesarios(self.cantidad_de_conexiones)
        self.hosts_que_se_pueden_albergar = (2 ** self.bits_necesarios) - 2
        self.rango = ''

    def Buscar_bits_necesarios(self, cantidad_de_conexiones: int):
        contador = 1
        for a in range(0, 100):
            if cantidad_de_conexiones <= (2 ** a):
                return contador - 1
            contador += 1

    def __Mostrar__(self, ip: str):
        print(ip)

class Direccionamiento:
    def __init__(self, direccion_privada):
        self.lista_de_subredes = []
        self.lista_de_subredes_internas = []
        self.lista_completa = []
        self.cantidad_de_subredes = 0
        self.cantidad_de_subredes_internas = 0
        self.cantidad_total = 0
        barra = direccion_privada.rfind('/')
        self.direccion_privada_decimal = direccion_privada[:barra]
        self.octetos_direccion_privada_decimal = self.direccion_privada_decimal.split('.')
        self.direccion_privada_binario = self.DDAB(self.octetos_direccion_privada_decimal)
        self.mascara_reducida = direccion_privada[barra + 1:]
        self.mascara_binario = self.CMDAMB(int(self.mascara_reducida))
        self.octetos_mascara_binario = self.mascara_binario.split('.')
        self.mascara_decimal = self.DBADD(self.octetos_mascara_binario)
        self.mascara_clase = ''
        self.mascara_tipo = True  # true->fija, false->variable
        self.mascara_fija = ''
        self.octetos_direccion_privada_binario = self.direccion_privada_binario.split('.')
        self.octetos_mascara_decimal = self.mascara_decimal.split('.')
        self.bits_para_hosts = 32 - int(self.mascara_reducida)
        self.bits_para_nuevas_subredes = 0
        self.bits_mayor_subred = 0


# DETERMINAR CANTIDAD TOTAL
    def Total(self):
        self.cantidad_total = self.cantidad_de_subredes_internas + self.cantidad_de_subredes


# AGREGAR UNA SUBRED A LA LISTA

    def add(self, red: subred = None, red_interna: subred_interna = None):
        if red_interna is not None:
            self.lista_de_subredes_internas.append(red_interna)
            self.cantidad_de_subredes_internas += 1
            self.lista_de_subredes_internas.sort(key=lambda x: x.cantidad_de_conexiones, reverse=True)
        if red is not None:
            red.name = nameSubred[self.cantidad_de_subredes]
            self.lista_de_subredes.append(red)
            self.cantidad_de_subredes += 1
            self.lista_de_subredes.sort(key=lambda x: x.cantidad_de_conexiones, reverse=True)


# CONVERTIR DIRECCION DECIMAL EN BINARIA

    def DDAB(self, octetos_decimal):
        ip_binario = self.NDAOB(int(octetos_decimal[0])) + '.' + self.NDAOB(int(octetos_decimal[1])) + '.' + self.NDAOB(int(octetos_decimal[2])) + '.' + self.NDAOB(int(octetos_decimal[3]))
        return ip_binario


# CONVERTIR NUMERO DECIMAL A OCTETO BINARIO

    def NDAOB(self, numero_decimal: int):
        octeto = ''
        contador = 7
        for i in range(0, 8):
            potencia = 2 ** contador
            if numero_decimal >= potencia:
                octeto += '1'
                numero_decimal = numero_decimal % potencia
                contador -= 1
            elif numero_decimal < potencia:
                octeto += '0'
                contador -= 1
        return octeto


# CONVERTIR OCTETO BINARIO A NUMERO DECIMAL

    def OBAD(self, octeto_binario):
        decimal = 0
        potencia = 7
        for i in octeto_binario:
            if i == '1':
                decimal += (2 ** potencia)
                potencia -= 1
            elif i == '0':
                potencia -= 1
        return str(decimal)


# CONVERTIR DIRECCION BINARIA A DIRECCION DECIMAL

    def DBADD(self, octetos_binarios):
        direccion_decimal = self.OBAD(octetos_binarios[0]) + '.' + self.OBAD(octetos_binarios[1]) + '.' + self.OBAD(octetos_binarios[2]) + '.' + self.OBAD(octetos_binarios[3])
        return direccion_decimal


# CONVERTIR MASCARA REDUCIDA A MASCARA BINARIO:

    def CMDAMB(self, mascara_reducida: int):
        mascara_binario = ''
        if int(mascara_reducida) <= 8:
            mascara_reducida += 0
        elif mascara_reducida <= 16:
            mascara_reducida += 1
        elif mascara_reducida <= 24:
            mascara_reducida += 2
        elif mascara_reducida <= 32:
            mascara_reducida += 3
        for i in range(0,35):
            if i < mascara_reducida:
                if i == 8 or i == 17 or i == 26:
                    mascara_binario += ('.')
                else:
                    mascara_binario += ('1')
            else:
                if i == 8 or i == 17 or i == 26:
                    mascara_binario += ('.')
                else:
                    mascara_binario += ('0')
        return mascara_binario


# BUSCAR LA CANTIDAD DE BITS NECESARIOS PARA CIERTO NUMERO

    def Buscar_bits(self, numero):
        contador = 1
        for i in range(0, 100):
            if numero <= 2 ** i:
                return contador -1
            contador += 1


# DETERMINAR SI LA MASCARA ES FIJA O VARIABLE:

    def Determinar_mascara_tipo(self):
        if (self.bits_para_nuevas_subredes + self.bits_mayor_subred) <= self.bits_para_hosts:
            self.mascara_tipo = True
        else:
            self.mascara_tipo = False


# DETERMINAR MASCARA FIJA:

    def DMF(self, mascara_en_binario, bits_necesarios):
        mascara_aux = list(mascara_en_binario)
        contador = 0
        for i in range(0, mascara_aux.__len__()):
            if mascara_aux[i] == '0' and contador < int(bits_necesarios):
                mascara_aux[i] = '1'
                contador += 1
        mascara_en_binario = ''.join(mascara_aux)
        return mascara_en_binario


#DETERMINAR EL RANGO

    def this_range_subred(self, red, tipo_de_puerta_de_enlace): # 1 si es mas q la netw 2 si es menos que la broad
        if tipo_de_puerta_de_enlace == 1:
            if red.cantidad_de_gateways == 1:
                rango1 = self.Gate(red.gateway_en_binario)
                rango2 = self.Gate_por_defecto(red.broadcast_en_binario)
            else:
                rango1 = self.Gate(red.gateway_en_binario[red.cantidad_de_gateways - 1])
                rango2 = self.Gate_por_defecto(red.broadcast_en_binario)
        else:
            if red.cantidad_de_gateways == 1:
                rango1 = self.Gate(red.network_en_binario)
                rango2 = self.Gate_por_defecto(red.gateway_en_binario)
            else:
                rango1 = self.Gate(red.network_en_binario)
                rango2 = self.Gate_por_defecto(red.gateway_en_binario[red.cantidad_de_gateways - 1])

        rango = self.DBADD(rango1.split('.')) + ' - ' + self.DBADD(rango2.split('.'))
        return rango

#DETERMINAR EL RANGO

    def this_range_subred_interna(self, red): # 1 si es mas q la netw 2 si es menos que la broad
        rango1 = self.Gate(red.network_en_binario)
        rango2 = self.Gate_por_defecto(red.broadcast_en_binario)
        rango = self.DBADD(rango1.split('.')) + ' - ' + self.DBADD(rango2.split('.'))
        return rango


# DETERMINAR MASCARA VARIABLE

    def DMV(self, red):
        red.mascara_reducida = 32 - red.bits_necesarios
        red.mascara_en_binario = self.CMDAMB(red.mascara_reducida)


# DETERMINAR LOS BITS DE LA ZONA DE CADA NUEVA SUBRED DE NETWORK:

    def Netw_mascara_variable(self, octetos_ntw_anterior, cantidad_de_bits):
        octeto1 = int(octetos_ntw_anterior[0])
        octeto2 = int(octetos_ntw_anterior[1])
        octeto3 = int(octetos_ntw_anterior[2])
        octeto4 = int(octetos_ntw_anterior[3])

        octeto4 += 2 ** cantidad_de_bits
        if octeto4 > 255:
            division = int(octeto4 / 255)
            resto = octeto4 % division
            octeto4 = resto
            octeto3 += division
            if octeto3 > 255:
                division1 = int(octeto3 / 255)
                resto1 = octeto3 % division1
                octeto3 = resto1
                octeto2 += division1
                if octeto2 > 255:
                    division2 = int(octeto2 / 255)
                    resto2 = octeto2 % division2
                    octeto2 = resto2
                    octeto1 += division2
                    
        return (str(octeto1) + '.' + str(octeto2) + '.' + str(octeto3) + '.' + str(octeto4))


# DETERMINAR LOS BITS QUE OCUPA LA NUEVA FRACCION DE MASCARA PARA AGREGARLA A LA MASCARA PREDETERMINADA

    def bits_de_netw(self, numero_decimal: int, cantidad_de_bits: int):
        bits_de_subred = ''
        numero_decimal -= 1
        contador = cantidad_de_bits - 1
        for i in range(0, cantidad_de_bits):
            potencia = 2 ** contador
            if numero_decimal >= potencia:
                bits_de_subred += '1'
                numero_decimal = numero_decimal % potencia
                contador -= 1
            elif numero_decimal < potencia:
                bits_de_subred += '0'
                contador -= 1
        return bits_de_subred


# DETERMINAR NETWORK DEL SIGUIENTE:

    def Determinar_siguiente(self, network_en_binario: str, cantidad_de_bits: str, mascara_red: int = None):
        ip_del_siguiente = self.Netw(ip_en_binario=network_en_binario, bits_de_sub=cantidad_de_bits, mascara_red=mascara_red)
        return ip_del_siguiente


# ASIGNAR NETWORK:

    def Netw(self, ip_en_binario, numero: int = None, bits_de_sub: int = None, mascara_red: int = None):
        if bits_de_sub is None:
            bits = self.bits_para_nuevas_subredes
            bits_de_subred = self.bits_de_netw(numero, self.bits_para_nuevas_subredes)
        else:
            bits = bits_de_sub
            bits_de_subred = self.bits_de_netw(bits_de_sub, bits_de_sub)
        contador = 0
        ip_aux = list(ip_en_binario)
        if mascara_red is None:
            mascara_reducida = int(self.mascara_reducida)
        else:
            mascara_reducida = mascara_red
        if mascara_reducida <= 8:
            mascara_reducida += 0
        elif mascara_reducida <= 16:
            mascara_reducida += 1
        elif mascara_reducida <= 24:
            mascara_reducida += 2
        elif mascara_reducida <= 32:
            mascara_reducida += 3
        for i in range(0, 35):
            if i < mascara_reducida:
                if i == 8 or i == 17 or i == 26:
                    ip_aux[i] = '.'
                else:
                    ip_aux[i] = ip_aux[i]
            else:
                if i == 8 or i == 17 or i == 26:
                    ip_aux[i] = '.'
                else:
                    if contador < bits:
                        ip_aux[i] = bits_de_subred[contador]
                        contador += 1
                    else:
                        ip_aux[i] = '0'
        retorno = ''.join(ip_aux)
        return retorno


# ASIGNAR BROADCAST:

    def Broad(self, ip_en_binario, numero: int, bits_para_nuevas_subredes = None):
        if bits_para_nuevas_subredes is None:
            bits = self.bits_para_nuevas_subredes
        else:
            bits = bits_para_nuevas_subredes
        contador = 0
        ip_aux = list(ip_en_binario)
        mascara_reducida = int(self.mascara_reducida)
        if mascara_reducida <= 8:
            mascara_reducida += 0
        elif mascara_reducida <= 16:
            mascara_reducida += 1
        elif mascara_reducida <= 24:
            mascara_reducida += 2
        elif mascara_reducida <= 32:
            mascara_reducida += 3
        for i in range(0, 35):
            if i < mascara_reducida:
                if i == 8 or i == 17 or i == 26:
                    ip_aux[i] = '.'
                else:
                    ip_aux[i] = ip_aux[i]
            else:
                if i == 8 or i == 17 or i == 26:
                    ip_aux[i] = '.'
                else:
                    if contador < bits:
                        ip_aux[i] = ip_aux[i]
                        contador += 1
                    else:
                        ip_aux[i] = '1'
        retorno = ''.join(ip_aux)
        return retorno


# ASIGNAR GATEWAY:

    def Gate(self, ip): # la ip en binario
        octetos = ip.split('.')
        octeto4 = int(self.OBAD(octetos[3]))
        octeto4 += 1
        if octeto4 == 256:
            octeto4 = 0
            octeto3 = int(self.OBAD(octetos[2]))
            octeto3 += 1
            octeto3str = self.NDAOB(octeto3)
            octeto4str = self.NDAOB(octeto4)
            ip = octetos[0] + '.' + octetos[1] + '.' + octeto3str + '.' + octeto4str
        else:
            octeto4str = self.NDAOB(octeto4)
            ip = octetos[0] + '.' + octetos[1] + '.' + octetos[2] + '.' + octeto4str
        return str(ip)


# ASIGNAR GATEWAY COMO UNO MENOS QUE LA PUERTA DE ESCAPE:

    def Gate_por_defecto(self, ip): # la ip en binario
        octetos = ip.split('.')
        octeto4 = int(self.OBAD(octetos[3]))
        octeto4 -= 1
        if octeto4 == -1:
            octeto4 = 0
            octeto3 = int(self.OBAD(octetos[2]))
            octeto3 -= 1
            octeto3str = self.NDAOB(octeto3)
            octeto4str = self.NDAOB(octeto4)
            ip = octetos[0] + '.' + octetos[1] + '.' + octeto3str + '.' + octeto4str
        else:
            octeto4str = self.NDAOB(octeto4)
            ip = octetos[0] + '.' + octetos[1] + '.' + octetos[2] + '.' + octeto4str
        return str(ip)


# CREAR LISTA GENERAL DE SUBREDES Y SUBREDES INTERNAS:

    def Crear_Lista(self):
        self.lista_completa = self.lista_de_subredes + self.lista_de_subredes_internas
        self.lista_completa.sort(key=lambda x: x.cantidad_de_conexiones, reverse=True)


# DIRECCIONAR subred_interna:

    def Direccionar_subred_interna(self, red: subred_interna, numero: int):
        red.mascara_en_binario = self.mascara_fija
        red.mascara_reducida = str(self.mascara_reducida) + str(self.bits_para_nuevas_subredes)
        red.mascara_en_decimal = self.DBADD(red.mascara_en_binario.split('.'))
        red.network_en_binario = self.Netw(ip_en_binario=self.direccion_privada_binario, numero=numero)
        red.network = self.DBADD(red.network_en_binario.split('.'))
        red.broadcast_en_binario = self.Broad(red.network_en_binario, numero)
        red.broadcast = self.DBADD(red.broadcast_en_binario.split('.'))
        red.rango = self.this_range_subred_interna(red)


# ASIGNAR BROADCAST POR MASCARA VARIABLE:

    def Broad_mascara_variable(self, network, cantidad_de_bits_para_hosts):
        if cantidad_de_bits_para_hosts > 8:
            cantidad_de_bits_para_hosts += 1
        if cantidad_de_bits_para_hosts > 16:
            cantidad_de_bits_para_hosts += 1
        if cantidad_de_bits_para_hosts > 24:
            cantidad_de_bits_para_hosts += 1
        lista = list(network)
        a = -1
        for i in range(0, cantidad_de_bits_para_hosts):
            if i == 8 or i == 17 or i == 25:
                lista[a] = '.'
            else:
                lista[a] = '1'
            a -= 1
        return ''.join(lista)


# DIRECCIONAR LAS SUBREDES INTERNAS POR MASCARA VARIABLE:

    def Direccionar_subred_interna_mascara_variable(self, red: subred, numero: int, numero_de_subredes):
        self.DMV(red)
        red.mascara_en_decimal = self.DBADD(red.mascara_en_binario.split('.'))
        red.network = self.Netw_mascara_variable(self.lista_completa[numero_de_subredes - 2].network.split('.'), self.lista_completa[numero_de_subredes - 2].bits_necesarios)
        red.network_en_binario = self.DDAB(red.network.split('.'))
        red.broadcast_en_binario = self.Broad_mascara_variable(red.network_en_binario, red.bits_necesarios)
        red.broadcast = self.DBADD(red.broadcast_en_binario.split('.'))
        red.rango = self.this_range_subred_interna(red)


# DIRECCIONAR subred:

    def Direccionar_subred_mascara_variable(self, red: subred, numero: int, cantidad_de_gate: int, tipo_de_puertas_de_enlace: int):
        self.DMV(red)
        red.mascara_en_decimal = self.DBADD(red.mascara_en_binario.split('.'))
        if numero == 1:
            red.network_en_binario = self.Netw(ip_en_binario=self.direccion_privada_binario, numero=numero, mascara_red=red.mascara_reducida)
            red.network = self.DBADD(red.network_en_binario.split('.'))
        else:
            red.network = self.Netw_mascara_variable(self.lista_de_subredes[numero - 2].network.split('.'), self.lista_de_subredes[numero - 2].bits_necesarios)
            red.network_en_binario = self.DDAB(red.network.split('.'))
        red.broadcast_en_binario = self.Broad_mascara_variable(red.network_en_binario, red.bits_necesarios)
        red.broadcast = self.DBADD(red.broadcast_en_binario.split('.'))
        if tipo_de_puertas_de_enlace == 2:
            if cantidad_de_gate == 1:
                red.gateway_en_binario = self.Gate_por_defecto(red.broadcast_en_binario)
                red.gateway = self.DBADD(red.gateway_en_binario.split('.'))
            else:
                for i in range(0, cantidad_de_gate):
                    if i == 0:
                        red.gateway_en_binario[i] = self.Gate_por_defecto(red.broadcast_en_binario)
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
                    else:
                        red.gateway_en_binario[i] = self.Gate_por_defecto(red.gateway_en_binario[i - 1])
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
        else:
            if cantidad_de_gate == 1:
                red.gateway_en_binario = self.Gate(red.network_en_binario)
                red.gateway = self.DBADD(red.gateway_en_binario.split('.'))
            else:
                for i in range(0, cantidad_de_gate):
                    if i == 0:
                        red.gateway_en_binario[i] = self.Gate(red.network_en_binario)
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
                    else:
                        red.gateway_en_binario[i] = self.Gate(red.gateway_en_binario[i - 1])
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
        red.rango = self.this_range_subred(red, tipo_de_puertas_de_enlace)


# DIRECCIONAR subred :

    def Direccionar_subred(self, red: subred, numero: int, cantidad_de_gate: int, tipo_de_puertas_de_enlace: int):
        red.mascara_en_binario = self.mascara_fija
        red.mascara_reducida = int(self.mascara_reducida) + int(self.bits_para_nuevas_subredes)
        red.mascara_en_decimal = self.DBADD(red.mascara_en_binario.split('.'))
        red.network_en_binario = self.Netw(self.direccion_privada_binario, numero)
        red.network = self.DBADD(red.network_en_binario.split('.'))
        red.broadcast_en_binario = self.Broad(red.network_en_binario, numero)
        red.broadcast = self.DBADD(red.broadcast_en_binario.split('.'))
        if tipo_de_puertas_de_enlace == 2:
            if cantidad_de_gate == 1:
                red.gateway_en_binario = self.Gate_por_defecto(red.broadcast_en_binario)
                red.gateway = self.DBADD(red.gateway_en_binario.split('.'))
            else:
                for i in range(0, cantidad_de_gate):
                    if i == 0:
                        red.gateway_en_binario[i] = self.Gate_por_defecto(red.broadcast_en_binario)
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
                    else:
                        red.gateway_en_binario[i] = self.Gate_por_defecto(red.gateway_en_binario[i - 1])
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
        else:
            if cantidad_de_gate == 1:
                red.gateway_en_binario = self.Gate(red.network_en_binario)
                red.gateway = self.DBADD(red.gateway_en_binario.split('.'))
            else:
                for i in range(0, cantidad_de_gate):
                    if i == 0:
                        red.gateway_en_binario[i] = self.Gate(red.network_en_binario)
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
                    else:
                        red.gateway_en_binario[i] = self.Gate(red.gateway_en_binario[i - 1])
                        red.gateway[i] = self.DBADD(red.gateway_en_binario[i].split('.'))
        red.rango = self.this_range_subred(red, tipo_de_puertas_de_enlace)


# A DIRECCIONAR!:

    def run(self, tipo_de_puerta_de_enlace: int):
        if self.cantidad_de_subredes != 0 and self.cantidad_de_subredes_internas != 0:
            self.Total()
            self.Crear_Lista()
            self.bits_para_nuevas_subredes = self.Buscar_bits(self.cantidad_total)
            self.bits_mayor_subred = self.Buscar_bits(self.lista_de_subredes[0].cantidad_de_conexiones)
            self.Determinar_mascara_tipo()
            self.mascara_fija = self.DMF(self.mascara_binario, self.bits_para_nuevas_subredes)
            if self.bits_para_hosts >= self.bits_para_nuevas_subredes:
                if self.mascara_tipo is True:
                    mostrando = '*******************************************************[Fixed-length subnetting]*****************************************************************'
                    i = 0
                    j = 0
                    while i < self.cantidad_total:
                        if i < self.cantidad_de_subredes:
                            self.Direccionar_subred(self.lista_de_subredes[i], i + 1, self.lista_de_subredes[i].cantidad_de_gateways, tipo_de_puerta_de_enlace)
                            i += 1
                        else:
                            self.Direccionar_subred_interna(self.lista_de_subredes_internas[j], i + 1)
                            j += 1
                            i += 1
                else:
                    mostrando = '*****************************************************[Variable-length subnetting]****************************************************************'
                    i = 0
                    j = 0
                    while i < self.cantidad_total:
                        if i < self.cantidad_de_subredes:
                            self.Direccionar_subred_mascara_variable(red=self.lista_de_subredes[i], numero=(i + 1), cantidad_de_gate=self.lista_de_subredes[i].cantidad_de_gateways, tipo_de_puertas_de_enlace=tipo_de_puerta_de_enlace)
                            self.Direccionar_subred_mascara_variable
                            i += 1
                        else:
                            self.Direccionar_subred_interna_mascara_variable(self.lista_de_subredes_internas[j], j + 1, i + 1)
                            j += 1
                            i += 1
                return mostrando
            else:
                print('Error: The subnetting is no posible!')
        else:
            print('Error: There are no subnets or interfaces!')


# INTERFAZ GRAFICA:
# COMPROBAR QUE LA DIRECCION IP ESTE ESCRITA CORRECTAMENTE:

def Comprobar_IP(ip: str):
    booleano = True
    barra = ip.rfind('/')
    mascara = int(ip[barra + 1:])
    ip_ = ip[:barra]
    octetos = ip_.split('.')
    if octetos.__len__() != 4: #comprobando si estan los 4 octetos
        booleano = False
    elif mascara < 0 or mascara > 32: #comprobando si la mascara esta correcta
        booleano = False
    #comprobando si los octetos son numericos
    elif not octetos[0].isalnum() or not octetos[1].isalnum() or not octetos[2].isalnum() or not octetos[3].isalnum():
        booleano = False
    #comprobando si los octetos estan correctos (entre 0 y 255)
    elif int(octetos[0]) > 255 or int(octetos[0]) < 0:
        booleano = False
    elif 0 > int(octetos[1]) or int(octetos[1]) > 255:
        booleano = False
    elif 0 > int(octetos[2]) or int(octetos[2]) > 255:
        booleano = False
    elif 0 > int(octetos[3]) or int(octetos[3]) > 255:
        booleano = False
    elif ip_.count('.') != 3:
        booleano = False
    return booleano


# COMPROBAR LA CANTIDAD DE HOSTS:

def comprobar_hosts(hosts):
    if type(hosts) is int:
        return True
    return False


# COMPROBAR SI EL NOMBRE DEL ROUTER NO HA SIDO ASIGNADO:

def Comprobar_nombre_de_router(red: Direccionamiento, R1: str, R2: str):
    nombre = R1 + '-' + R2
    r1_r2 = []
    r1_r2.append(R1)
    r1_r2.append(R2)
    for y in range(0, red.cantidad_de_subredes_internas):
        if red.lista_de_subredes_internas[y].name == nombre:
            flag = True
            while flag:
                print(f'Error: The interface {nombre} it is already done! Try again:')
                r1 = str(input(f'Type the name of the first router: '))
                r2 = str(input(f'Type the name of the second router: '))
                nombre = r1 + '-' + r2
                if nombre != red.lista_de_subredes_internas[y].name:
                    flag = False
                    r1_r2.clear()
                    r1_r2.append(r1)
                    r1_r2.append(r2)
                else:
                    r1_r2 = Comprobar_nombre_de_router(red, r1, r2)
    return r1_r2


def mayor_que_cero(cantidad):
    if cantidad < 0:
        return False
    return True


# COMPROBAR IP BINARIA:
def CompIpBin(ip):
    octetos = ip.split('.')
    if octetos.__len__() != 4:
        return False
    for a in range(0, 3):
        if octetos[a].__len__() != 8:
            return False
        for i in octetos[a]:
            if i != '0' and i != '1':
                return False
    return True

# MOSTRAR LA TABLA EN LA TERMINAL:

def Mostrar(RED: Direccionamiento, mensaje):
    os.system('clear')
    print(mensaje)
    tabla = PrettyTable(['Name','Hosts','Conec','Bits', 'Mask', 'Network', 'Gateway', 'Broadcast', 'Range'])
    for i in range(0, RED.cantidad_total):
        tabla.add_row([RED.lista_completa[i].name,RED.lista_completa[i].cantidad_de_hosts,RED.lista_completa[i].cantidad_de_conexiones,RED.lista_completa[i].bits_necesarios,RED.lista_completa[i].mascara_en_decimal,RED.lista_completa[i].network,RED.lista_completa[i].gateway,RED.lista_completa[i].broadcast, RED.lista_completa[i].rango])
    print(tabla)
    print('*************************************************************************************************************************************************')
def DecABin(iP):
        d = Direccionamiento('10.10.10.10/24')
        ip_binaria = d.DDAB(iP.split('.'))
        print(ip_binaria)
        return

def BinADec(iP):
        d = Direccionamiento('10.10.10.10/24')
        ip_decimal = d.DBADD(iP.split('.'))
        print(ip_decimal)
        return

def print_progress_bar(progress):
    bar_length = 70
    progress = int(progress * bar_length)
    bar = ['x' if i < progress else ' ' for i in range(bar_length)]
    print('[' + ''.join(bar) + ']')
def barra():
# Actualización progresiva de la barra de carga
        for i in range(71):
            progress = i / 70
            print_progress_bar(progress)
        
            print('''  _____ _    _ ____  _   _ ______ _______ _______ _____ _   _  _____ 
 / ____| |  | |  _ \| \ | |  ____|__   __|__   __|_   _| \ | |/ ____|
| (___ | |  | | |_) |  \| | |__     | |     | |    | | |  \| | |  __ 
 \___ \| |  | |  _ <| . ` |  __|    | |     | |    | | | . ` | | |_ |
 ____) | |__| | |_) | |\  | |____   | |     | |   _| |_| |\  | |__| |
|_____/ \____/|____/|_| \_|______|  |_|     |_|  |_____|_| \_|\_____|
                                                                     
                                                                     ''')
            print_progress_bar(progress)
            time.sleep(2/70)
            os.system('clear')


# PETICION DE LOS VALORES NECESARIOS:
def MENU():
    barra()
    os.system('clear')
    print('######################################################################')
    print('''  _____ _    _ ____  _   _ ______ _______ _______ _____ _   _  _____ 
 / ____| |  | |  _ \| \ | |  ____|__   __|__   __|_   _| \ | |/ ____|
| (___ | |  | | |_) |  \| | |__     | |     | |    | | |  \| | |  __ 
 \___ \| |  | |  _ <| . ` |  __|    | |     | |    | | | . ` | | |_ |
 ____) | |__| | |_) | |\  | |____   | |     | |   _| |_| |\  | |__| |
|_____/ \____/|____/|_| \_|______|  |_|     |_|  |_____|_| \_|\_____|
                                                                     
                                                                     ''')
    print('######################################################################')
    os.system('sleep 0.5')
    opcion = int(input('[OPTIONS]:\n1-[SUBNETTING]\n2-[CONVERT DECIMAL IP TO BINARY IP]\n3-[CONVERT BINARY IP TO DECIMAL IP]\nChose an option: '))
    if opcion == 1:
        menu()
    elif opcion == 2:
        flag = True
        while flag:
            iP = input('Type the decimal IP: ')
            comp = iP + '/24'
            if Comprobar_IP(comp):
                DecABin(iP)
                flag = False
            else:
                print('The IP is wrong, try again')
            
    elif opcion == 3:
        flag = True
        while flag:
            iP = input('Type the binary IP: ')
            if CompIpBin(iP):
                BinADec(iP)
                flag= False
            else:
                print('The IP is worng, try again')

def menu():
        ip = input('type the IP address range (Ex: 192.148.12.0/24): ')
        if Comprobar_IP(ip):
            Red = Direccionamiento(ip)
            cantidad_de_subredes = int(input('Type how many subnets you wants to build: '))
            while comprobar_hosts(cantidad_de_subredes) == False:
                cantidad_de_subredes = int(input(('Error, you should type a number, try again: ')))
            cantidad_de_routers = int(input('Type how many interfaces (connections beetwen routers) your network will have: '))
            while comprobar_hosts(cantidad_de_routers) == False:
                cantidad_de_subredes = int(input(('Error, you should type a number, try again: ')))
            bandera = int(input('Type one (1) to assign the gateways as one address more than the network address or two (2) for one less than broadcas address: '))
            while bandera != 1 and bandera != 2:
                bandera = int(input('Error: invalid input, try again:'))
            
            for i in range(0, cantidad_de_subredes):
                cantidad_de_hosts = int(input(f'Type how many hosts your network {i + 1} will have: '))
                cantidad_de_puertas_de_enlace = int(input('Type the number of gateways: '))
                Subred = subred(cantidad_de_hosts, cantidad_de_puertas_de_enlace)
                Red.add(red=Subred)
            for i in range(0, cantidad_de_routers):
                flag = True
                R1 = str(input(f'Type the name of the first router on interface{i + 1} : '))
                R2 = str(input(f'Type the name of the second router on interface {i + 1} : '))
                if Red.cantidad_de_subredes_internas != 0:
                    r1_r2 = Comprobar_nombre_de_router(Red, R1, R2)
                    R1 = r1_r2[0]
                    R2 = r1_r2[1]
                Subred = subred_interna(R1, R2)
                Red.add(red_interna=Subred)
            mensaje = Red.run(bandera)
            Mostrar(Red, mensaje)
        else:
            print('Error: Direccion IP incorrecta!')
            menu()
MENU()

