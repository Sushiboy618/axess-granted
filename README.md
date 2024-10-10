# axess-granted
Ce projet est un client pour le service La Vie Scolaire, il permet notamment le détournement de certaines utilisations
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
		raise NotImplementedError
	elif choix == "4" : 
		load()
	else : 
		print("\033[1;31mERREUR\033[0m")
print("\033[1;31m______________________________________________\033[0m")
	



