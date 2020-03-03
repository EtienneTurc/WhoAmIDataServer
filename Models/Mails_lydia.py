#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import re

from utils import tag_mail


# In[2]:


df = pd.read_json(r'data/gmail_boetto_basic.txt', encoding = 'utf-8')


# In[57]:


df['cat'] = df.headers.apply(tag_mail)

df.loc[df.cat == 'lydia']


# In[43]:


import plotly.express as px

mails_lydia = df.loc[df.cat=='lydia'][['date', 'body']]

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

mails_lydia['montant'] = mails_lydia.body.apply(find_price)

mails_lydia['cumsum'] = mails_lydia.montant.cumsum()
 
mails_lydia_cpy = mails_lydia.loc[mails_lydia.montant.isna() == False].copy()

fig = px.line(mails_lydia_cpy, x='date', y='cumsum')
fig.show()


# In[49]:


mails_lydia = mails_lydia.loc[mails_lydia.montant.isna()==False]


# In[52]:


mails_lydia['date'].values


# In[60]:


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


# In[61]:


lydia(df)


# In[ ]:


def lydia(df):
	def find_price(x):
	    res1 = re.findall(r"vous a regle \d+ €", x)
	    res2 = re.findall(r" \d+ € payes a", x)
	    if len(res1) == 1:
	        return int(re.findall(r"\d+", res1[0])[0])/100
	    elif len(res2) == 1:
	        return - int(re.findall(r"\d+", res2[0])[0])/100
	    else:
	        return None

	mails_lydia = df.loc[df.cat=='lydia'][['date', 'body']]
	mails_lydia['montant'] = mails_lydia.body.apply(find_price)

