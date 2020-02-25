"""
		Utils compiles utility scripts for the analysis of the emails
"""
def tag_mail(header):
	"""
	tag_mail will tag if the mail is in the list of structured emails

	input:
	header : is the header of the email
	output:
	name of the category, or 'no_cat' if non were find

	usage example: df['cat'] = df.headers.apply(tag_mail)
	"""
	comp_list = ['linkedin', 'facebook', 'lydia', 'spotify', 'sncf', 'twitter', 'tinder', 'deezer', 'itunes',
				 'apple', 'google','uber','ubereats','doctolib', 'instagram', 'amazon']

	if header == []:
		return 'no_cat'
	for k in header:
		if k['name'] == 'From':
			L_cat = [el * (el in k['value']) for el in comp_list]
			L_cat = list(filter(lambda x: x!='', L_cat))
			if L_cat == []:
				return('no_cat')
			elif len(L_cat) > 2:
				print(L_cat)
				return L[cat[0]]
			elif len(L_cat) == 1:
				return L_cat[0]
			else:
				return 'no_cat'

