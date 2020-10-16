## Test mails on haveibeenpwn and return results

import requests, xlsxwriter
from bs4 import BeautifulSoup
from time import strftime, gmtime, sleep 

from colorama import init, Fore, Back, Style
init()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


## A lancer avec un fichier emails.txt qui contient un ensemble de mail
## Le script check si les mails ont fuités sur haveibeenpwned et retourne le nom des breaches
## Le résultat est stocké dans un fichier excel output-searchOnHIBP.xlsx


def prRed(skk): print(Fore.RED + "[!] {}".format(skk) + Style.RESET_ALL) 
def prGreen(skk): print(Fore.GREEN + "[*] {}".format(skk) + Style.RESET_ALL) 
def prInfo(skk): print(Fore.CYAN + "[*] {}".format(skk) + Style.RESET_ALL) 



def checkEmail(mail,session,row,col):

	headers = {
        'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",        
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		'Accept-Language': "en-US,en;q=0.5",
		'Accept-Encoding': "gzip, deflate",
		'Connection': "close",
		'Upgrade-Insecure-Requests': "1"
        }

	url = "https://haveibeenpwned.com/unifiedsearch/"+mail
	response = session.get(url,headers=headers,verify=False)
	prInfo("Test pour "+mail)
	worksheet.write_string(row,col,mail)
	col += 1

	breaches = ''
	if response.status_code == 200:
		prGreen("Breaches trouvées!")
		site_json = response.json()
		for key in range(len(site_json["Breaches"])):
			for value in site_json["Breaches"][key]:
				if value == "Name" :
					prGreen(value+" : "+site_json["Breaches"][key][value])
					breaches = breaches + site_json["Breaches"][key][value] + " ; "
		worksheet.write_string(row,col,breaches)
	else:
		prRed("Aucune fuite d'informations.")
		worksheet.write_string(row,col,"None")



excel = xlsxwriter.Workbook('output-searchOnHIBP.xlsx') 
worksheet = excel.add_worksheet("Have i been pwned") 
row=0
col=0

worksheet.write(row,col,"Adresse :")
col += 1
worksheet.write(row,col,"Fuites :")



f = open("emails.txt", "r")

startTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print("Start : " + startTime)

emails = []

session = requests.Session()

'''
# Ajout de proxy burp pour du debug
session.proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080"
}
'''


for x in f:
	emails.append(x.rstrip())
for mail in emails:
	col=0
	row += 1
	checkEmail(mail,session,row,col)				
	sleep(3)
endTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
print("End : " + endTime)
excel.close()
print("Résultats sauvegardés dans "+"output-searchOnHIBP.xlsx")



