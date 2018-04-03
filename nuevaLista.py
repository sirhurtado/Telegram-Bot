import telebot
import time
from telebot import types

# Variables globales
bot = telebot.TeleBot("562967459:AAHRQIiwwh7n8r6lfhbcuzcJIl188h87noU")
listaJugadoresRaid = []
sitioRaid = ""

##################
# Comando /start #
##################
@bot.message_handler(commands=['start'])
def bienvenida(message):
        bot.reply_to(message, "Hola, soy el bot que te facilitará la experiencia en Pokémon Go" + "\n\n¿Qué puedo hacer por ti?" + "\n/ayuda - Muestra todos los comandos disponibles")

#######################
# Comando /nuevaLista #
#######################
@bot.message_handler(commands=['nuevalista'])
def crearLista(mensaje):
        try:
                chatID = mensaje.chat.id
                markup = types.ForceReply(selective=True)
                hora = bot.send_message(chatID, "<b>Indica la hora y el gimnasio donde se realizará el Raid</b> \n\n" + "Debe tener el siguiente formato: \n" + "<i>ej. 12:00 - Casa Olesa</i>", parse_mode="HTML", reply_markup=markup)
                bot.register_next_step_handler(hora, registrarHora)
        except:
                bot.send_message(mensaje, "Error")

# Obtener la respuesta del usuario
def registrarHora(mensaje):
        chatID = mensaje.chat.id
        respuesta = mensaje.text

        hora = respuesta[:5]
        horaError = "<b>DEBES ESCRIBIR CORRECTAMENTE LA HORA</b>"

        if (comprobarHora(hora)):
                global sitioRaid
                sitioRaid = respuesta
                empezarLista(mensaje)
        else:
                bot.reply_to(mensaje, horaError + "\n\n", parse_mode="HTML")
                crearLista(mensaje)

# Comprobar el formaro de la hora
def comprobarHora(hora):
        try:
                time.strptime(hora, '%H:%M')
        except:
                return False
        else:
                return True

# Crear la lista
def empezarLista(mensaje):
        try:
                chatID = mensaje.chat.id
                mensajeID = mensaje.message_id
                usuarioID = mensaje.from_user.id
                usuario = mensaje.from_user
                listaJugadoresRaid.clear()
                global sitioRaid
                accionesLista = types.InlineKeyboardMarkup()
                apuntar = types.InlineKeyboardButton("Apúntame", callback_data='Apuntado')
                eliminar = types.InlineKeyboardButton("Elimíname", callback_data='Eliminado')
                accionesLista.add(apuntar, eliminar)
                bot.send_message(chatID, "<b>" + sitioRaid.upper() + "</b>", reply_markup=accionesLista, parse_mode="HTML", disable_web_page_preview=True)
        except:
                bot.send_message(chatID, "No se ha podido crear la lista correctamente")

@bot.callback_query_handler(func=lambda call: call.data == 'Apuntado')
def unirJugador(call):
        try:
                chatID = call.message.chat.id
                mensajeID = call.message.message_id
                usuarioID = call.from_user.id
                usuario = call.from_user
                if usuario.first_name not in listaJugadoresRaid:
                        listaJugadoresRaid.append(usuario.first_name)
                        accionesLista_editada = types.InlineKeyboardMarkup()
                        apuntar = types.InlineKeyboardButton("Apúntame", callback_data='Apuntado')
                        eliminar = types.InlineKeyboardButton("Elimíname", callback_data='Eliminado')
                        accionesLista_editada.add(apuntar, eliminar)
                        bot.edit_message_text("<b>" + sitioRaid.upper() + "</b>\n\n<b>Lista de jugadores (" + str(len(listaJugadoresRaid)) + "):</b> \n" + imprimirJugadores(listaJugadoresRaid), chatID, mensajeID, reply_markup=accionesLista_editada, parse_mode="HTML")
                        bot.answer_callback_query(call.id, text="¡Te has unido a la lista!")
                else:
                        bot.answer_callback_query(call.id, text="¡Ya estás apuntado en la lista!")
        except:
                bot.send_message(chatID, "¿Sigue existiendo esta lista? Prueba a crear una nueva /nuevaLista")

@bot.callback_query_handler(func=lambda call: call.data == 'Eliminado')
def unirJugador(call):
        try:
                chatID = call.message.chat.id
                mensajeID = call.message.message_id
                usuarioID = call.from_user.id
                usuario = call.from_user
                if usuario.first_name in listaJugadoresRaid:
                        listaJugadoresRaid.remove(usuario.first_name)
                        accionesLista_editada = types.InlineKeyboardMarkup()
                        apuntar = types.InlineKeyboardButton("Apúntame", callback_data='Apuntado')
                        eliminar = types.InlineKeyboardButton("Elimíname", callback_data='Eliminado')
                        accionesLista_editada.add(apuntar, eliminar)
                        bot.edit_message_text("<b>" + sitioRaid.upper() + "</b>\n\n<b>Lista de jugadores (" + str(len(listaJugadoresRaid)) + "):</b> \n" + imprimirJugadores(listaJugadoresRaid), chatID, mensajeID, reply_markup=accionesLista_editada, parse_mode="HTML")
                        bot.answer_callback_query(call.id, text="¡Ya has sido borrado de la lista!")
                else:
                        bot.answer_callback_query(call.id, text="¡No estás apuntado en la lista!")
        except:
                bot.send_message(chatID, "¿Sigue existiendo esta lista? Prueba a crear una nueva /nuevaLista")

def imprimirJugadores(lista):
        mensaje = ""
        for jugador in lista:
                mensaje = mensaje + str(jugador) + "\n"
        return mensaje

# COMANDO /BORRARLISTA
@bot.message_handler(commands=['borrarlista'])
def borrarLista(mensaje):
        listaJugadoresRaid.clear()
        bot.reply_to(mensaje, text="Lista borrada correctamente!")


# COMANDO /AYUDA
@bot.message_handler(commands=['ayuda'])
def bienvenida(message):
        mensaje = ""
        mensaje = "Estos son los comandos disponibles: \n"
        mensaje = mensaje + "/nuevaLista - Crea una lista nueva \n"
        mensaje = mensaje + "/borrarLista - Borra una lista"
        bot.reply_to(message, mensaje)

# Ejecutar el bot
bot.polling()
