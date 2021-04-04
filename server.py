#coding: utf-8

#version python: 3.8

from settings import *
from datetime import datetime
import mimetypes

#Non utiliser sur ce site web
def selecteur_cookies(environ, selecteur):
	"""Selectionne un cookie, si il existe renvoi la valeur du selecteur si non None"""
	try:
		dic = dict(x.split("=") for x in environ["HTTP_COOKIE"].split("; "))

		for clef, valeur in dic.items():
			if clef == selecteur:
				return valeur
	except:
		return None


def index(environ, start_response):
	"""Page index du site web"""
	
	description = "Mon CV"
	keywords = "CV, MARZIN Samuel"
	
	start_response("200 OK", [("Content-type", "text/html; charset=" + SERVER_CHARSET)])

	with open("html/template.html", "r") as fichier:
		template = fichier.read()
	
	with open("html/index.html", "r") as fichier:
		index = fichier.read()
	
	template = template.format(charset=SERVER_CHARSET, description=description, keywords=keywords, main=index, date=datetime.today().year)
	
	yield bytes(template, SERVER_CHARSET)


def creations(environ, start_response):
	"""Page <mes créations> du site web"""
	
	description = "Mes créations"
	keywords = "Créations, Informatique, MARZIN Samuel"
	
	start_response("200 OK", [("Content-type", "text/html; charset=" + SERVER_CHARSET)])

	with open("html/template.html", "r") as fichier:
		template = fichier.read()
	
	with open("html/creations.html", "r") as fichier:
		index = fichier.read()
	
	template = template.format(charset=SERVER_CHARSET, description=description, keywords=keywords, main=index, date=datetime.today().year)
	
	yield bytes(template, SERVER_CHARSET)


def apropos(environ, start_response):
	"""Page <à propos> du site web"""
	
	description = "À propos du site web."
	keywords = "infos, MARZIN Samuel"
	
	start_response("200 OK", [("Content-type", "text/html; charset=" + SERVER_CHARSET)])

	with open("html/template.html", "r") as fichier:
		template = fichier.read()
	
	with open("html/apropos.html", "r") as fichier:
		index = fichier.read()
	
	template = template.format(charset=SERVER_CHARSET, description=description, keywords=keywords, main=index, date=datetime.today().year)
	
	yield bytes(template, SERVER_CHARSET)


mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("application/vnd.sqlite3", ".sqlite3")
mimetypes.add_type("application/x-pem-file", ".pem")
def ressource(environ, start_response):
	"""La fonction ressource permet de naviger des les fichiers du site sans à avoir à créer des URLs, de plus on empèche les fichiers non publique d'être servi (type "python" par exemple) avec un filtre.
Cette fonction ne peut être utiliser que dans une application WSGI."""

	lien_ressource = environ["PATH_INFO"]

	with open(lien_ressource[1:], "br") as fichier:
		ressource = fichier.read()

	type_fichier = mimetypes.MimeTypes().guess_type(lien_ressource)[0]

	if not DEBUG and (type_fichier == "text/x-python" or type_fichier == "application/x-python-code" or type_fichier == "application/x-python-bytecode" or type_fichier == "application/sql" or type_fichier == "application/x-pem-file"):
		return erreur("403", environ, start_response)
	elif type_fichier == None:
		start_response("200 OK", [("Content-type", "application/octet-stream")])
	else:
		start_response("200 OK", [("Content-type", f"{type_fichier}; charset=" + SERVER_CHARSET)])

	return [ressource]


def erreur(code, environ, start_response):
	"""Génère une page d'erreur HTTP"""
	
	description = ""
	keywords = ""
	date = "2021"

	with open("html/template.html", "r") as fichier:
		template = fichier.read()
	
	if code == "404":
		start_response("404 NOT FOUND", [("Content-Type", "text/html; charset=" + SERVER_CHARSET)])

		code_description = "La page que vous recherchez n'existe plus ou n'a jamais existé!"
	elif code == "403":
		start_response("403 FORBIDDEN", [("Content-Type", "text/html; charset=" + SERVER_CHARSET)])

		code_description = "Vous n'avez pas l'autorisation d'accéder à cette ressource!"
	elif code == "503":
		start_response("503 SERVICE UNAVALABLE", [("Content-Type", "text/html; charset=" + SERVER_CHARSET)])

		code_description = "Le site est temporairement inaccessible pour des raisons de maintenance!"
	else:
		start_response("500 INTERNAL SERVER ERROR", [("Content-Type", "text/html; charset=" + SERVER_CHARSET)])

		code_description = "Le serveur rencontre un problème technique! Nous travaillons activement à la résolution de ce problème..."
	
	with open("html/erreur_http.html", "r") as fichier:
		erreur_http = fichier.read().format(code=code, code_description=code_description)
	
	template = template.format(charset=SERVER_CHARSET, description=description, keywords=keywords, main=erreur_http, date=date)

	yield bytes(template, SERVER_CHARSET)


#Les urls
urls = {"/": index,
	"/index": index,
	"/creations": creations,
	"/apropos": apropos}


#applicaction executable
def application(environ, start_response):
	"""Aplication executable"""
	try:
		return ressource(environ, start_response)
	except:
		pass

	try:
		if MAINTENANCE:
			return erreur("503", environ, start_response)
		
		for url, fonction in urls.items():
			if environ["PATH_INFO"] == url:
				return fonction(environ, start_response)

		return erreur("404", environ, start_response)
	except:
		return erreur("500", environ, start_response)


#Serveur de test (ne pas activer en production)
if __name__ == "__main__":
	if DEBUG:
		from wsgiref.simple_server import make_server

		httpd = make_server("", PORT, application)

		print(f"Le serveur de test est actif sur le port: {PORT}.")

		httpd.serve_forever()
	else:
		print("Pour démarer le serveur de test vous devez metre la variable \"DEBUG\" qui se trouve dans le fichier \"settings.py\" sur \"True\".")
