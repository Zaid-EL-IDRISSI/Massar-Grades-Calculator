import requests
from bs4 import BeautifulSoup as Bfs
print("Hello user, this program was made by Zaid El Idrissi.")
print("Connecting, please wait.")
def vergulfloat(InputNum):
    str(InputNum)
    if InputNum.find(",") != -1:
        return InputNum[0:InputNum.find(",")] + "." + InputNum[InputNum.find(",") + 1:len(InputNum)]
    else:
        return InputNum
def m_fr(Num):
    if type(Num) == int:
        output = str(Num) +"/1"
    elif type(Num) == float:
        Num = str(Num)
        if int(Num[Num.find(".")+1:len(Num)]) == 0:
             output = Num[0:Num.find(".")] + "/1"
        elif int(Num[0:Num.find(".")]) == 0:
            lenn = str(int(Num[Num.find(".")+1:len(Num)]))
            output = lenn + "/" + str(pow(10,len(lenn)))
        else:
             output = Num.replace(".","") + "/" + str(pow(10,len(Num) - Num.index(".") - 1))
    return output
def op_fr(Nume1,Nume2,operateur):
    a = int(Nume1[0:Nume1.find("/")])
    b = int(Nume1[Nume1.find("/") + 1:len(Nume1)])
    c = int(Nume2[0:Nume2.find("/")])
    d = int(Nume2[Nume2.find("/") + 1:len(Nume2)])
    if operateur in ["+","-","*"]:
        Denomurateur = b*d
        if operateur == "+":
            Nemurateur = (a*d)+(c*b)
        elif operateur == "-":
            Nemurateur = (a*d)-(c*b)
        else:
             Nemurateur = a*c
    elif operateur == "/":
        Nemurateur = a*d
        Denomurateur = b * c
    return  str(Nemurateur) + "/" + str(Denomurateur)
def fRtn(fr):
    return int(fr[0:fr.find("/")])/int(fr[fr.find("/") + 1:len(fr)])
def Majeuré(nmbr):
    nmbr = str(nmbr)
    if len(nmbr) > 5:
        if int(nmbr[5]) <= 5:
            nmbr = nmbr[0:5]
        else:
            nmbr = nmbr[0:4] + str(int(nmbr[4]) + 1)
    return float(nmbr)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0 (Edition std-2)",
        "sec-ch-ua-platform":"Windows",
        "Sec-Fetch-Mode":"navigate",
}
cookies = {".AspNetCore.Culture":"c=fr-FR|uic=fr-FR"}
session = requests.Session()
session.cookies.update(cookies)
login_url = "https://massarservice.men.gov.ma/moutamadris/Account"
login_url_post = "https://massarservice.men.gov.ma/moutamadris/Account/Login"
url_GetBulletins = "https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetBulletins"
login_page = session.get(login_url,headers=headers)
login_page_soup = Bfs(login_page.text, "html.parser")
token = login_page_soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
if token is None:
    print("Sorry, there is no (token) !")
    exit()
payload_login = {"__RequestVerificationToken":token,
                 "UserName":input("Veuillez entrer votre nom d'utilisateur :"),
                 "Password":input("Veuillez entrer votre mot de passe :")}
response_login = session.post(login_url_post,data=payload_login,headers=headers)
response_login_soup = Bfs(response_login.text, "html.parser")
chekking  = response_login_soup.find('h1',class_='welcomeUser')
if chekking is not None and chekking.find('span').text == "Bonjour":
    print(f"Connection successful :)\nHello {chekking.span.next_sibling.text}.")
else:
    print("Connection failed :(\nPlease check your username and password !")
    exit()
payload_GetBulletins = {"Annee":input("Please enter the year of the season :"),
                        "IdSession":input("Please choose :\n1 : first semester.\n2 : second semester.\n>>>")}

response_Bulletins = session.get(url_GetBulletins,params=payload_GetBulletins,headers=headers)
response_Bulletins_soup = Bfs(response_Bulletins.text, 'html.parser')
cheking2 = response_Bulletins_soup.find_all('dd')
if len(cheking2[1]) != 0 and payload_GetBulletins.get("IdSession") in ["1","2"]:
    print("The grades have been obtained :)")
    etb = cheking2[0].text
    lvl = cheking2[1].text
    print(f"Your institution is :{etb}\nYour level is :{lvl}")
else:
    print("The entered information is invalid :(\nPlease check and try again !")
    exit()
print("Grade calculation...")
soupe = response_Bulletins_soup.find("tbody").find_all("tr")
dict = {}
for tr in soupe:
    tr = Bfs(str(tr),'html.parser').find_all("td")
    count = 0
    NumCon = "0/1"
    moyen_t = "0/1"
    moyen_matieres = "0/1"
    activite = "none"
    Name_of_matier = "none"
    for td in tr :
        if str(Bfs(str(td), 'html.parser').find("span")) != "None":
             span = str(Bfs(str(td), 'html.parser').find("span").string)
        else:
             span = "None"
        
        if count == 0:
                Name_of_matier = Bfs(str(td), 'html.parser').string
                dict[Name_of_matier] = 0
        elif count >= 1 and count <= 3:
             if span != "None":
                  moyen_t = op_fr(moyen_t,m_fr(float(vergulfloat(span))),"+")
                  NumCon = op_fr(NumCon,m_fr(1),"+")
        elif count == 4:
             if span != "None":
                  activite = m_fr(float(vergulfloat(span)))
        elif count == 5:     
             if span != "None":
                  moyen_t = op_fr(moyen_t,m_fr(float(vergulfloat(span))),"+")
                  NumCon = op_fr(NumCon,m_fr(1),"+")
             if activite == "none":
                  moyen_matieres = op_fr(moyen_t,NumCon,"/")
             else:
                  if Name_of_matier == "LANGUE ANGLAISE":
                       CoefCont = 0.6
                       CoefAct = 0.4
                  else:
                       CoefCont = 0.75
                       CoefAct = 0.25
                  moyen_matieres = op_fr(op_fr(op_fr(moyen_t,NumCon,"/"),m_fr(CoefCont),"*"),op_fr(activite,m_fr(CoefAct),"*"),"+")
        count += 1
    dict.update({Name_of_matier:moyen_matieres})
moyen_generale = 0
SomeCoefficient = 0
for element in dict:
    tmp = int(input(f"Enter the coefficient >{element}< :"))
    moyen_generale += Majeuré(fRtn(dict.get(element)))*tmp
    SomeCoefficient += tmp
    print("Average :",Majeuré(fRtn(dict.get(element))))
moyen_generale = Majeuré(moyen_generale / SomeCoefficient)
print("Overall average :",moyen_generale)





