from flask import Flask, render_template, request, redirect
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
import validators
import json
import util
import logging


app = Flask(__name__)
app.debug = True
app.secret_key = b'xen_o7q536_*88^j-)m$pyyp*gmq$()8!p*ral@+k5+_=^jnjd'

csrf = CSRFProtect(app)
socketio = SocketIO(app)

@app.route("/")
def index():

	app.logger.info("Pozvan view index");

	ime_i_prezime = Config.name + ' ' + Config.surname
	return render_template("index.html", name = ime_i_prezime)


@app.route("/djelatnosti")
def djelatnosti():

	app.logger.info("Pozvan view djelatnosti");
	return render_template("djelatnosti.html")
	
	
@app.route("/kontakt")
def kontakt():
	app.logger.info("Pozvan view kontakt");
	return render_template("kontakt.html") 	
	

@app.route("/chat")
def chat():  
	
	app.logger.info("Pozvan view chat");
	return render_template("chat.html")

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@app.route("/bankAccount")
def bankovni_racun():
	ime_banke = Config.banka
	broj_racuna = Config.iban	
	
	if not util.provjeri_iban(broj_racuna):
		broj_racuna = "Neispravan IBAN!"
	
	app.logger.info("Pozvan view bankAccount");
	return render_template("bankAccount.html", banka=ime_banke, iban=broj_racuna)


@app.route("/comments", methods=['get', 'post'])
def komentari():
	
	komentari = []
	poruka = ''
	
	# Učitavamo komentare iz datoteke
	with open('komentari.json', mode='r', encoding='utf-8') as json_datoteka:
		komentari = json.load(json_datoteka)
		json_datoteka.close()
	
	ime = ''
	komentar = ''
	
	# Ako je metoda POST onda podatke validiramo i spremamo
	if request.method == 'POST':
		ime = request.form["ime"]
		komentar = request.form["komentar"]
		
		if len(ime)<3 or len(komentar)<3:
			ispravan_unos = False
			poruka = 'Pogrešan unos.'
		else:
			ispravan_unos = True
			poruka = 'Uspješan unos.'
			
		# Zapisujemo komentare u datoteku
		if ispravan_unos:
			with open('komentari.json', mode='w', encoding='utf-8') as json_datoteka:
				komentari.append({"ime": ime, "komentar": komentar})
				json.dump(komentari, json_datoteka)
				json_datoteka.close()
				
				# Da ne radi dupli POST prilikom refreshanja stranice
				# (https://en.wikipedia.org/wiki/Post/Redirect/Get)
				return redirect("/comments")
	
	# Prikazujemo podatke
	
	app.logger.info("Pozvan view komentari");
	return render_template("comments.html", komentari=komentari, poruka=poruka, ime=ime, komentar=komentar)


if __name__ == "__main__":
	formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
	
	handler = logging.FileHandler('mjermenLog.log')
	handler.setLevel(logging.INFO)
	handler.setFormatter(formatter)
	
	app.logger.addHandler(handler)
	socketio.run(app, debug=True)
	app.run()

	

