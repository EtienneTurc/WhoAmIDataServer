import re
import pandas as pd

services = open("services.txt", "r").read().split("\n")
services = [s.strip() for s in services if s]

def lydia(df):
    def find_price(x):
        res1 = re.findall(r"VOUS A RÉGLÉ \d+,\d+ €", x)
        res2 = re.findall(r"\d+,\d+ € PAY", x)
        res3 = re.findall(r"VOUS AVEZ RÉGLÉ \d+,\d+ €", x)
        if len(res1) == 1:
            return float(re.findall(r"\d+,\d+", res1[0])[0].replace(',','.'))
        elif len(res2) == 1:
            return - float(re.findall(r"\d+,\d+", res2[0])[0].replace(',','.'))
        elif len(res2) == 1:
            return - float(re.findall(r"\d+,\d+", res3[0])[0].replace(',','.'))
        else:
            return None

    mails_lydia = df.loc[df.cat=='lydia'][['date', 'body']]
    
    if mails_lydia.shape[0] == 0:
        return {'date' : [],
                'transaction' : []
               }

    mails_lydia['transaction'] = mails_lydia.body.apply(find_price)
    mails_lydia = mails_lydia.loc[mails_lydia.transaction.isna()==False]

    return {'date' : list(mails_lydia['date'].values),
            'transaction' : list(mails_lydia['transaction'].values)
            }

from datetime import datetime
import locale
try : 
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8") # if error here set it to fr_FR or check locale -a
except :
    locale.setlocale(locale.LC_TIME, "fr_FR") # if error here set it to fr_FR or check locale -a


def doctolib(df):
    #function to apply to retrieve date
    def get_date(x):
        tmp = x['snippet']
        tmp = tmp.split(x['appointment'])[1]
        tmp = tmp.split(' DÉPLACER')[0]
        try:
            date = datetime.strptime(tmp, '%A %d %B à %Hh%M')
            date = date.replace(year = x['date'].year)
        except:
            date = None
        return date

    #restriction to doctolib mails
    mails_doc = df.loc[df.cat == 'doctolib']
    #restriction to confirmed appointments
    mails_doc = mails_doc.loc[mails_doc.snippet.str.contains("confirmé")]

    if mails_doc.shape[0] == 0:
        return {'date' : [],
                'appointment' : []
               }

    # Regex to match weekdays
    reg_weekdays = re.compile(r' Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche')

    # Extracting name of doctor + sector by splitting on confirmé and weekdays regex
    mails_doc['appointment'] = mails_doc.snippet.apply(lambda x: reg_weekdays.split(x.split('confirmé ')[1])[0] )

    # Retriving appointment date, the year is the one of the email notification
    mails_doc['cons_date'] = mails_doc[['snippet', 'date', 'appointment']].apply(get_date, axis = 1)

    #we discard wrong matchings
    mails_doc = mails_doc.loc[mails_doc['cons_date'].isna() == False]

    return {'date' : list(mails_doc['cons_date'].values),
            'appointment' : list(mails_doc['appointment'].values)
           }


def amazon(df):
    #restriction to amazon emails
    df_amazon = df.loc[df.cat=='amazon']
    #get all amazon orders
    df_amazon = df_amazon.loc[df_amazon.body.str.contains("Votre Expédition ")]

    res = []

    for el in df.body:
        tmp = {}
        
        # total cost parsing
        try:
            total_cost = re.findall(r'Montant total pour cet envoi : EUR \d{0,100000},\d\d', el)[0]
            tmp['total_cost'] = re.findall(r'\d{0,100000},\d\d',total_cost)[0]
        except:
            continue
        # payment tool parsing
        try:
            tmp['payment_tool'] = re.findall(r'Payé par (.*?): ', el)[0]
        except:
            tmp['payment_tool'] = ''
            
        # delivering date parsing
        try:
            date = re.findall(r'Livraison : \n (.*?) \n \n', el, re.DOTALL)[0]
            date = datetime.strptime(date, '%A %d %B %Y')
        except:
            date = None
        
        tmp['date'] = date
        
        #parsing products
        products = re.findall(r'\(Vendu par (.*?) \n \n', el, re.DOTALL)
        
        #if no product pass
        if products==[]:
            continue
        
        tmp['articles'] = []
        
        for prod in products:
            res_prod = {}
            res_prod['seller'] = prod.split(') :')[0]
            
            prod = prod.split('\n ')[1:]
            
            res_prod['article'] = prod[0]
            res_prod['price'] = re.findall(r'\d{0,100000},\d\d', prod[1])[0]
            
            tmp['articles'] += [res_prod]
        res += [tmp]
    return res

# Call each function referenced in the services.txt file
def extractServiceInfo(df):
    res = {}
    for s in services:
        s = s.strip()
        res[s] = globals()[s](df)
    return res
