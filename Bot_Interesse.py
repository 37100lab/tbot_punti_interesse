from telegram import *
from telegram.ext import *
import math as m
import psycopg2
import json

def dist(lat1,lon1, lat2, lon2):
    return 6371 * 2 * m.asin(m.sqrt(m.pow(m.sin((m.radians(lat2) - m.radians(lat1)) / 2), 2) + m.cos(lat1) * m.cos(lat2) * m.pow(m.sin((m.radians(lon2) - m.radians(lon1)) / 2), 2)))

def start(update: Update, context: CallbackContext) -> None:
    testo = "Benvenuto!!! \nQuesto bot ti permette di trovare il punto di interesse più vicino a te. \nInvia la tua posizione."
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo)

def distanza(update: Update, context: CallbackContext) -> None:
    try:
        lat1 = update.message.location.latitude
        lon1 = update.message.location.longitude
        d = []
        for i in range(0,len(coord_x)):
            d.append(dist(lat1,lon1,coord_x[i],coord_y[i]))
        e = d[:]        #uso e come copia
        d.sort()
        ind = 0
        for i in range(0,len(d)):
            if d[0]==e[i]:
                ind = i
                break
        testo = "Il punto di interesse più vicino è: " + nome[ind]
        testo_dist = "\nDistanza: " + str(round(d[0],2)) + " km"
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo+testo_dist)
        update.message.reply_location(coord_x[ind], coord_y[ind])
    except:
        testo_try = "Attenzione!!!\nInviare solo la posizione attuale.\nInterrompere la condivisione della posizione in tempo reale."
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo_try)

def echo(update: Update, context: CallbackContext) -> None:
    testo = "Non è un comando valido"
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo) #update.message.text per leggere il messaggio ricevuto

def main():
    updater = Updater("1921881808:AAHLJx0ehTZAYQx7IrZueO6azja47AAvalk")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.location, distanza))    #update.message.reply_location(10,10) metti coordinate del posto e invia

    updater.start_polling()

    updater.idle()

con = psycopg2.connect(
    host="127.0.0.1",       #192.168.20.20 IP locale    #3.142.202.105
    database="geoapp",
    user="postgres",
    password="plumake2021!"
)

cur = con.cursor()
v = []
coord_x = []
coord_y = []
nome = []

cur.execute("select ST_AsGeoJSON(geom) from puntidiinteresse")    #ricava coordinate in GeoJSON
a = cur.fetchall()
cur.execute("select nome from puntidiinteresse")    #ricava coordinate in GeoJSON
b = cur.fetchall()
for i in range(0,len(a)):
    v.append(json.loads(a[i][0]))
    coord_x.append(v[i]['coordinates'][1])
    coord_y.append(v[i]['coordinates'][0])
    nome.append(b[i][0])
cur.close()
con.close()
main()
