import requests, random
from time import sleep
requests.packages.urllib3.disable_warnings()

# -- http basic auth --

account = 'XXX.myshopify.com/admin/gift_cards.json'
key = 'apikey'
pwd = 'apipwd'

# -- end http basic auth --

# -- begin functions section --

def ran_char():
  a_z = list(range(65,91))
  random.shuffle(a_z)
  l = random.randint(0, 25)
  y = a_z[l]
  return(y)

def ran_part(r_len):
	i = 0
	r_p= ''
	while i < r_len:
		r_p += chr(ran_char())
		i += 1
	return(r_p)

def seq_part(c_len,r_len,nr):
	s_p = ''
	s_len = c_len - r_len
	pad_req = s_len - len(str(nr))
	t = 0
	while t < pad_req:
		s_p += '0'
		t += 1
	s_p += str(nr)
	return(s_p)

def code(cod_len,ran_len,num):
	gc_code = ran_part(ran_len) + '-' + seq_part(cod_len,ran_len,num) 
	return(gc_code)

# -- end functions section --

# -- main --

gc_codes = input("How many codes would you like to create: ")
gc_len = input("How long should the code be: ")
gc_ran = input("How long should the random part be: ")
gc_value = input("What is the card value: ")

q = 0
while q < gc_codes:
	x = code (gc_len,gc_ran,q+1)
	print x
	gc_data = { "gift_card": { "note": "auto generated", "initial_value": gc_value, "code": x } }
	s = requests.post(account, json=gc_data,  auth=(key,pwd))
	if s.status_code != '201' :
	  print s.status_code
	sleep(0.05)
	q += 1

# -- end main --
