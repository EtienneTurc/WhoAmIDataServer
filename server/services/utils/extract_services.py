from datetime import datetime
import locale
import re
import pandas as pd

services = open("services.txt", "r").read().split("\n")
services = [s.strip() for s in services if s]


def lydia(df):
    def find_price(x):
        res1 = re.findall(r"VOUS A RÉGLÉ \d+,\d+ EU", x)
        res2 = re.findall(r"\d+,\d+ EU PAY", x)
        res3 = re.findall(r"VOUS AVEZ RÉGLÉ \d+,\d+ EU", x)
        if len(res1) == 1:
            return float(re.findall(r"\d+,\d+", res1[0])[0].replace(',', '.'))
        elif len(res2) == 1:
            return - float(re.findall(r"\d+,\d+", res2[0])[0].replace(',', '.'))
        elif len(res2) == 1:
            return - float(re.findall(r"\d+,\d+", res3[0])[0].replace(',', '.'))
        else:
            return None

    mails_lydia = df.loc[df.cat == 'lydia'][['date', 'body']]

    if mails_lydia.shape[0] == 0:
        return []

    mails_lydia['amount'] = mails_lydia.body.apply(find_price)
    mails_lydia = mails_lydia.loc[mails_lydia.amount.isna() == False]

    return mails_lydia[['date', 'amount']].to_dict('records')
    # {'date' : list(mails_lydia['date'].values),
    #         'transaction' : list(mails_lydia['transaction'].values)
    #         }


try:
    # if error here set it to fr_FR or check locale -a
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
except:
    # if error here set it to fr_FR or check locale -a
    locale.setlocale(locale.LC_TIME, "fr_FR")


def doctolib(df):
    mails_doc = df.loc[df.cat == 'doctolib']

    mails_doc = mails_doc.loc[mails_doc.snippet.str.contains("confirme")]

    res = []

    for date_mail, el in mails_doc.loc[:, ['date', 'body']].itertuples(index=False):
        date = datetime.fromtimestamp(int(date_mail)/1000)
        tmp = {}

        try:
            name = re.findall(r'RDV confirme \n \n(.*?) \n', el)[0]
        except:
            name = None
        tmp['name'] = name

        try:
            spe = re.findall(name + ' \n(.*?) \n', el)[0]
        except:
            spe = None
        tmp['spe'] = spe

        try:
            date = re.findall(spe + ' \n(.*?) \n', el)[0]
            date = datetime.strptime(date, '%A %d %B a %Hh%M')
            date = date.replace(year=date_mail.year)
            tmp['date'] = str(int(date.timestamp()*1000))
        except:
            date = None
            tmp['date'] = None

        try:
            address = re.findall(
                r"Acces & informations \n \n(.*?) \n \nOBTENIR L'ITINERAIRE", el, re.DOTALL)[0]
            address = ''.join(address.split('\n'))
        except:
            address = None
        tmp['address'] = address

        res += [tmp]
    return res


def amazon(df):
    # restriction to amazon emails
    df_amazon = df.loc[df.cat == 'amazon']
    # get all amazon orders
    df_amazon = df_amazon.loc[df_amazon.body.str.contains("Votre Expédition ")]

    res = []

    for el in df.body:
        tmp = {}
        # total cost parsing
        try:
            amount = re.findall(
                r'Montant total pour cet envoi : EUR \d{0,100000},\d\d', el)[0]
            amount = re.findall(r'\d{0,100000},\d\d', amount)[0]
            # replacing the , with . if necessary
            amount = amount.replace(",", ".")
            tmp['amount'] = float(amount)
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

        # converting to unix millisecs
        tmp['date'] = str(date.timestamp()*1000)

        # parsing products
        products = re.findall(r'\(Vendu par (.*?) \n \n', el, re.DOTALL)

        # if no product pass
        if products == []:
            continue

        tmp['articles'] = []

        for prod in products:
            res_prod = {}
            res_prod['seller'] = prod.split(') :')[0]

            prod = prod.split('\n ')[1:]

            res_prod['article'] = prod[0]
            price = re.findall(r'\d{0,100000},\d\d', prod[1])[0]
            # replacing the , with . if necessary
            price = price.replace(",", ".")
            res_prod['price'] = float(price)

            tmp['articles'] += [res_prod]
        res += [tmp]
    return res


def uber_rides(df):
    df_uber = df.loc[df.cat == 'uber']

    res = []

    for date, el in df_uber.loc[:, ['date', 'body']].itertuples(index=False):
        date = datetime.fromtimestamp(int(date)/1000)
        tmp = {}
        # place
        try:
            departure, destination = re.findall(
                r'\d{1,2}:\d{1,2} (.*?) \d{1,2}:\d{1,2} (.*?) Invitez', el)[0]
            tmp['departure'] = departure
            tmp['destination'] = destination
        except:
            continue

        # price
        try:
            price = re.findall(r' Total: \d{1,1000},\d{2,1000} EU ', el)[0]
            price = re.findall(r'\d{1,1000},\d{2,1000}', price)[0]
            tmp['price'] = price
        except:
            price = None
            tmp['price'] = price
            pass

        # distance
        try:
            distance = re.findall(r'\d{1,1000}.{0,1}\d{0,1000} km', el)[0]
            tmp['distance'] = distance
        except:
            distance = None
            tmp['distance'] = distance
            pass

        # date
        try:
            horaire = re.findall(r'\d{1,2}:\d\d', el)
            start = datetime.strptime(horaire[0], '%H:%M')
            end = datetime.strptime(horaire[1], '%H:%M')
            start = start.replace(
                year=date.year, month=date.month, day=date.day)
            end = end.replace(year=date.year, month=date.month, day=date.day)
            tmp['start'] = str(int(start.timestamp()*1000))
            tmp['end'] = str(int(end.timestamp()*1000))
        except:
            start = None
            end = None
            tmp['start'] = start
            tmp['end'] = end
            pass

        res += [tmp]

    return res


def uber_bicycle(df):
    df_uber = df.loc[df.cat == 'uber']

    df_uber = df_uber.loc[df_uber.body.str.contains("velos electriques")]

    res = []

    for date, el in df_uber.loc[:, ['date', 'body']].itertuples(index=False):
        date = datetime.fromtimestamp(int(date)/1000)
        tmp = {}
        # place
        try:
            departure, destination = re.findall(
                r'\d{1,2}:\d\d (.*?) \d{1,2}:\d\d (.*?) contacter l\'assistance', el)[0]
            tmp['departure'] = departure
            tmp['destination'] = destination
        except:
            continue

        # price
        try:
            price = re.findall(r' Total: \d{1,1000},\d{2,1000} EU ', el)[0]
            price = re.findall(r'\d{1,1000},\d{2,1000}', price)[0]
            tmp['price'] = price
        except:
            price = None
            tmp['price'] = price
            pass

        # distance
        try:
            distance = re.findall(
                r'\d{1,1000}.{0,1}\d{0,1000} kilometres', el)[0]
            # r'\d{1,1000}.{0,1}\d{0,1000} kilomètres', el)[0]
            tmp['distance'] = distance
        except:
            distance = None
            tmp['distance'] = distance
            pass

        # date
        try:
            horaire = re.findall(r'\d{1,2}:\d\d', el)
            start = datetime.strptime(horaire[0], '%H:%M')
            end = datetime.strptime(horaire[1], '%H:%M')
            start = start.replace(
                year=date.year, month=date.month, day=date.day)
            end = end.replace(year=date.year, month=date.month, day=date.day)
            tmp['start'] = str(int(start.timestamp() * 1000))
            tmp['end'] = str(int(end.timestamp() * 1000))
        except:
            start = None
            end = None
            tmp['start'] = start
            tmp['end'] = end
            pass

        res += [tmp]

    return res


def uber_eats(df):
    df_uber = df.loc[:1, :]

    res = []
    for date, el in df_uber.loc[:, ['date', 'body']].itertuples(index=False):
        tmp = {}

        # price
        try:
            price = re.findall(r'Total: \d{1,1000},\d{2,1000} EU ', el)[0]
            price = re.findall(r'\d{1,1000},\d{2,1000}', price)[0]
            tmp['price'] = price
        except:
            price = None
            tmp['price'] = price
            pass

        # restaurant
        try:
            restaurant = re.findall(r'commandé chez (.*?)\.', el)[0]
            tmp['restaurant'] = restaurant
        except:
            tmp['restaurant'] = None
            pass

        # articles
        try:
            cmd = re.findall(r'Total (.*?) Montant facturé ', el, re.DOTALL)[0]
            articles = re.findall(
                r'\d{1,3} \n(.*?) \n\d{1,1000},\d\d EU', cmd, re.DOTALL)[:-1]
            tmp['articles'] = articles
        except:
            tmp['articles'] = None
            pass

        # date
        try:
            date = re.findall(
                r'Total: \d{1,1000},\d{2,1000} EU \n(.*?) \n', el)[0]
            date = datetime.strptime(date, '%a, %b %d, %Y')
            date = str(date.timestamp()*1000)
            tmp['date'] = date
        except:
            tmp['date'] = None
            pass

        res += [tmp]

    return res

# Call each function referenced in the services.txt file


def extract_services(df):
    res = {}
    for s in services:
        s = s.strip()
        res[s] = globals()[s](df)
    return res
