import re
import pandas as pd


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
	mails_lydia['transaction'] = mails_lydia.body.apply(find_price)
	mails_lydia = mails_lydia.loc[mails_lydia.transaction.isna()==False]

	return {'date' : list(mails_lydia['date'].values),
			'transaction' : list(mails_lydia['transaction'].values)
		   }

