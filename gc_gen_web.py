
import requests, random, bottle, os
from bottle import route, request, run, get, default_app, post, static_file, TEMPLATE_PATH, jinja2_view
from time import sleep
from ConfigParser import SafeConfigParser
from sys import argv

# suppress urllib3 errors
requests.packages.urllib3.disable_warnings()

# -- read login credentials  --
r_file = False
creds = SafeConfigParser()
creds.read('credentials.ini')

account = creds.get('main', 'account')
key = creds.get('main', 'key') 
pwd = creds.get('main', 'pwd') 
# -- end login creds section --

TEMPLATE_PATH[:] = ['templates']

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

@route('/static/css/<filename>')
def cssget(filename):
    return static_file(filename, root="./static/css")

@route('/static/js/<filename>')
def javaget(filename):
    return static_file(filename, root="./static/js")

@route('/static/fonts/<filename>')
def fontsget(filename):
    return static_file(filename, root="./static/fonts")

@route('/static/js/vendor/<filename>')
def modernget(filename):
    return static_file(filename, root="./static/js/vendor")

@route('/static/img/<filename>')
def faviconget(filename):
    return static_file(filename, root="./static/img")
@get('/')
def index():
    return 'I am alive!'

@route('/', name='home', method='GET')
@get('/<creds_file>')
@jinja2_view('index.html')
def index(creds_file = None):
    global r_file
    if creds_file == 'true':
        r_file = True
    return {'title':'GC-GEN'}

@get('/index')
@get('/index/<creds_file>')
def get_info(creds_file = None):
    global r_file
    if creds_file == 'true':
        r_file = True
        print 'r_file true'
    print creds_file
    return '''
        <form action="/convert" method="post">
                <p>Shopify account url (with endpoint)  <input name="gc_gen_account" type="text" /></p>
                <p>API KEY:  <input name="gc_gen_api_key" type="text" /></p>
                <p>API PWD:  <input name="gc_gen_api_pwd" type="text" /></p>
                <p>Nr of cards to be created:  <input name="gc_cards_nr" type="text" /></p>
                <p>Length of cards : <input name="gc_cards_length" type="text" /></p>
                <p>Value of cards : <input name="gc_cards_value" type="text" /></p>
            <input value="convert" type="submit" />
        </form>
    '''  
'''
@post('/convert')
def convert():

    int_nr_cards = int(request.forms.get('gc_cards_nr'))
    int_length_cards = int(request.forms.get('gc_cards_length'))
    int_value_cards = int(request.forms.get('gc_cards_value'))

    gc_ran = int_length_cards - (len(str(int_nr_cards))+1)   

    print 'processing'
    q = 1
    while q <= int_nr_cards:
        x = code(int_length_cards,gc_ran,q)
        print x
        gc_data = { "gift_card": { "note": "auto web generated", "initial_value": int_value_cards, "code": x } }
        print r_file
        if r_file:
            send_to_store(account,gc_data,key,pwd)
        else: 
            send_to_store(gc_gen_account,gc_data,gc_gen_api_key,gc_gen_api_pwd)
        q += 1 
    return "<p>Your cards have been created.</p>"
'''

@route('/result', method='POST')
@jinja2_view('result.html')
def result():
    int_nr_cards = int(request.forms.get('gc_cards_nr'))
    int_length_cards = int(request.forms.get('gc_cards_length'))
    int_value_cards = int(request.forms.get('gc_cards_value'))

    gc_ran = int_length_cards - (len(str(int_nr_cards))+1)   

    print 'processing'
    q = 1
    while q <= int_nr_cards:
        x = code(int_length_cards,gc_ran,q)
        print x
        gc_data = { "gift_card": { "note": "auto web generated", "initial_value": int_value_cards, "code": x } }
        print r_file
        if r_file:
            send_to_store(account,gc_data,key,pwd)
        else: 
            send_to_store(gc_gen_account,gc_data,gc_gen_api_key,gc_gen_api_pwd)
        q += 1 
    return "<p>Your cards have been created.</p>"

'''
run(host="localhost", port=8080)
'''

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

