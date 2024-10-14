############
#VS Scraper 0.1  #
############
### Importations des modules ###
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta

### Défintion des constantes ###
login_url = 'https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/WSAuth/connexion'
home_url = 'https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/WSDashboard/afficherDashboard'
note_url = 'https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/releveNote/releveNotes'
info_url = "https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/WSMenu/infosPortailUser"
homework_url = "https://ent05.la-vie-scolaire.fr/eliot-textes/vueCalendaire/eleve"
ID = {'idEleve': 8736}
login_data = {
    'login': 'toor', 
    'password': 'root', 
    'externalentpersjointure': None 
}
DATA0 = dict()
DATA1 = list()
DATA2 = list() # pas implemente
MOYG = list()
REALMOYG = list()

### Défintion des fonctions ###
def load():
	"""Charger DATA0,DATA1 et DATA2
	params : aucun
	return : aucun
	"""
	global DATA0,DATA1,DATA2
	print("[*] Récupération des infos...")
	DATA0 = getInfos()
	print("[*] Récupération des notes...")
	DATA1 = getData1()
	print("\033[34m[#] Récupération de l'emploi du temps...\033[0m")
	#a implementer
	print("\033[32m[+] Initialisation terminée\033[0m")

def analyzeNotesHTML(html):
	"""Extraire les notes du code html
	params : html>code a extraire
	return : [notes] liste des notes
	"""
	soup = BeautifulSoup(html, 'html.parser')
	table_releve = soup.find('table', 	class_='tableReleve')
	notes = []
	if table_releve:
	    rows = table_releve.find_all('tr')
	    for row in rows[1:]: 
	        cols = row.find_all('td')
	        if len(cols) == 2:
	            matiere_prof = cols[0].get_text(separator=' ').strip()
	            evaluation_note = cols[1].get_text(separator=' ').strip()
	            notes.append({
	                'matiere_prof': matiere_prof,
	                'evaluation_note': evaluation_note
	            })
	return notes

def getMatiereEtProf(raw):
	"""Retourner la matiere et le prof
	params : raw>str compliqué
	return : [matiere,prof]
	"""
	fuzed = [raw[0:20].strip(),raw[20:].strip()]
	matiere = fuzed[0]
	if "nsi" in matiere.lower():
		matiere = "Spécialité NSI"
	elif "histoire" in matiere.lower():
		matiere = "Histoire Géographie EMC"
	elif "pc" in matiere.lower():
		matiere = "Spécialité Physique Chimie"
	elif "math3" in matiere.lower():
		matiere = "Spécialité Mathématiques"
	elif "allemand" in matiere.lower():
		matiere = "Allemand LV2"
	elif "lv1" in matiere.lower():
		matiere = "Anglais LV1"
	elif "ens" in matiere.lower():
		matiere = "Enseignement scientifique"
	elif "eps" in matiere.lower():
		matiere = "EPS"
	elif "fra" in matiere.lower() : 
		matiere = "Français"
	prof = fuzed[1]
	return [matiere,prof]
	
def getNotes(raw):
	"""Retourner les notes d'une matiere'
	params : raw>str complique
	return : notedata
	"""
	global MOYG
	noteslist = raw.split('  - ')
	notedata = list()
	db = list()
	pattern = r'(.+)\s\((.+)\)\s:\s(.+)'
	for note in noteslist : 
		match_ = re.match(pattern,note)
		evaluation = match_.group(1).strip()
		date = match_.group(2)
		notecache = match_.group(3).replace(",",".")
		cache1 = notecache.split("/")
		cache2 = float(cache1[0])
		cache3 = float(cache1[1])
		cache4 = (cache2/cache3) * 20
		db.append(cache4)
		notedata.append([evaluation,date,notecache])
	locmoyg = sum(db)/len(db)
	MOYG.append(locmoyg)
	notedata.append(["Moyenne","trimestre",str(locmoyg) + "/20"])
	return notedata

def getData1():
	"""Recuperer toutes les donnes sur les notes
	params : aucun
	return : list > toutes les matieres, profs et notes
	"""
	global REALMOYG,MOYG
	MOYG = list()
	notespage = session.get(note_url)
	rawhtml = notespage.text
	rawdata = analyzeNotesHTML(rawhtml)
	finaldata = list()
	for elem in rawdata :
		matprof = elem['matiere_prof']
		matproflist = getMatiereEtProf(matprof)
		notes = elem['evaluation_note']
		data = getNotes(notes)
		finaldata.append([matproflist[0],matproflist[1],data])
	REALMOYG = sum(MOYG)/len(MOYG)
	return finaldata
	
def printNotes(data1):
	"""Afficher les notes
	params : data1
	return : aucun
	"""
	global REALMOYG
	print("###[NOTES]###")
	for elem in data1 : 
		print("Matiere : ",elem[0])
		print("Professeur : ",elem[1])
		print("Notes : ")
		for note in elem[2] : 
			print(f"{note[0]} du {note[1]} : {note[2]}")
		print("####################")
	print(f"\033[1;31mMOYENNE GENERALE : {round(REALMOYG,2)}\033[0m")

def getInfos() : 
	raw = session.get(info_url).text	
	data = json.loads(raw)
	info = {
        "etablissement": data.get("infoUser", {}).get("etabName", ""),
        "prenom": data.get("infoUser", {}).get("userPrenom", ""),
        "nom": data.get("infoUser", {}).get("userNom", ""),
        "profil": data.get("infoUser", {}).get("profil", "")
    }
	return info

def printInfos(data0) : 
	print("###[INFORMATIONS]###")
	print("Etablissement de l'eleve : ", data0['etablissement'])
	print("Prenom de l'eleve : ", data0['prenom'])
	print("Nom de l'eleve : ",data0["nom"])
	print("Profil : ",data0["profil"])


def getDay():
    # Obtenir la date actuelle
	aujourd_hui = datetime.today()
    # Trouver le début de la semaine (lundi)
	debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    # Trouver le lundi suivant
	lundi_suivant = debut_semaine + timedelta(days=7)
    # Retourner les dates au format 'AAAA-MM-JJ'
	return [debut_semaine.strftime('%Y-%m-%d'), lundi_suivant.strftime('%Y-%m-%d')]

def getHomeworks() :
	"""Renvoie les devoirs a faire pour le jour de cours suivant dans DATA2
	params : aucun
	return : aucun	
	"""
	global DATA2
	days = getDay()
	print(days)
	parameters = {'timeshift':-120,'from' : days[0], 'to' : days[1]}
	homeworks = session.get(homework_url,params = parameters)
	print(homeworks.text,homeworks)
### Programme principal ###

# Ouverture de la session
print("[*] Ouverture de la session...")
session = requests.Session()

# Intialisation
print("\033[1;31m###[La Vie Scolaire]###\033[0m")
print("[*] Connexion à la vie scolaire...")
connexion = session.post(login_url, json=login_data)
if connexion.ok:
	print("\033[32m[+] Connexion reussie\033[0m")
else : 
	print("\033[31m[-] Echec de la connexion\033[0m")
	raise Exception
load()



menu = """\033[1;32m
1) Afficher mes informations
2) Afficher mes notes
3) Afficher mes devoirs pour demain
4) Rafraichir
e) quitter\033[0m
[$] > """

while 1:
	print("\033[1;36m______________________________________________\033[0m")
	
	choix = str(input(menu))
	
	if choix == 'e' : 
		break
	elif choix == "1" : 
		printInfos(DATA0)
	elif choix == "2" : 
		printNotes(DATA1)
	elif choix == "3" : 
		getHomeworks()
	elif choix == "4" : 
		load()
	else : 
		print("\033[1;31mERREUR\033[0m")
print("\033[1;31m______________________________________________\033[0m")
