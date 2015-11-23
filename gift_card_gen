import requests, random
from time import sleep
from ConfigParser import SafeConfigParser

# suppress urllib3 errors
requests.packages.urllib3.disable_warnings()

# -- read login credentials  --
creds = SafeConfigParser()
creds.read('credentials.ini')

account = creds.get('main', 'account')
key = creds.get('main', 'key') 
pwd = creds.get('main', 'pwd') 
# -- end login creds section --

# -- begin functions section --
def ins_dash(string, index):
    return string[:index] + '-' + string[index:]

def ran_char():
  a_z = list(range(65,91))        # create a list with all values from 65 to 91
  random.shuffle(a_z)             # shuffle the list
  l = random.randint(0, 25)       # pick a random position in the randomized array
  y = a_z[l]                      # select the value
  return(y)

def ran_part(r_len):
	i = 0
	r_p= ''                       # initialise string variable
	while i < r_len:              
		r_p += chr(ran_char())    # fill up the string with random charcters 
		i += 1
	return(r_p)

def seq_part(c_len,r_len,nr):
	s_len = c_len - r_len         # determine length of seq part
	s_p = str(nr).zfill(s_len)    # pad seq part with zeroes
	return(s_p)

def code(cod_len,ran_len,num):
	gc_code = ran_part(ran_len) + seq_part(cod_len,ran_len,num)  # put code together 
	return(gc_code)

def get_input(question):
    numeric = False                         # initialise flag
    while numeric != True:                  # while flag not set, repeat
      try:                                  # try
     	 raw_in = raw_input(question)       # get raw input
     	 numeric = raw_in.isdigit()         # check ig input is numeric
     	 value = int(raw_in)                # change int to string
      except ValueError:                    # catch
         print("That's not a number.")      # warn if failed
    return(value)

def send_to_store(store,payload,apikey,apipwd):
	s = requests.post(store, json=payload,  auth=(apikey,apipwd))
	if s.status_code != 201:
		print s.status_code
	sleep(0.05)
	return()
# -- end functions section --

# -- main --
# get info from user
gc_codes = get_input("How many gift cards would you like to create: ")
gc_len = get_input("How long should the gift card code be: ")
# gc_ran = get_input("How long should the random part be (multiple of 4 preferred): ")  # random part is determined by user
gc_ran = gc_len - (len(str(gc_codes))+1)                                                # random part is calculated automatically
gc_value = get_input("What is the gift card $ value: ")

# process info
q = 1
while q <= gc_codes:
	x = code(gc_len,gc_ran,q)
	print x
	gc_data = { "gift_card": { "note": "auto generated 2", "initial_value": gc_value, "code": x } }
	send_to_store(account,gc_data,key,pwd)                    
	q += 1
# -- end main --

