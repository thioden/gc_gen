
import requests, random, bottle
from bottle import route, request, run, get
from time import sleep
from ConfigParser import SafeConfigParser
from sys import argv

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

# -- web server code --
@get('/')
def index():
    return 'I am alive!'

@route('/cards')
def get_info():
    return '''
        <form action="/cards" method="post">
            Nr of cards to be created:  <input name="gc_cards_nr" type="text" /></br>
            Length of cards : <input name="gc_cards_length" type="text" /></br>
            Value of cards : <input name="gc_cards_value" type="text" /></br>
            <input value="Submit" type="submit" />
        </form>
    '''

@route('/cards', method='POST')
def process_info():

    nr_cards = request.forms.get('gc_cards_nr')
    length_cards = request.forms.get('gc_cards_length')
    value_cards = request.forms.get('gc_cards_value')

    int_nr_cards = int(nr_cards)
    int_length_cards = int(length_cards)
    int_value_cards = int(value_cards)

    gc_ran = int_length_cards - (len(str(int_nr_cards))+1)   

    print ' ' + nr_cards + ' ' + value_cards
    q = 1
    while q <= int_nr_cards:
        x = code(int_length_cards,gc_ran,q)
        print x
        gc_data = { "gift_card": { "note": "auto web generated", "initial_value": int_value_cards, "code": x } }
        send_to_store(account,gc_data,key,pwd)                    
        q += 1 
    return "<p>Your cards have been created.</p>"


bottle.run(host='0.0.0.0', port=argv[1])

