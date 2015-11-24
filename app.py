from bottle import error, get, post, run, request, static_file, route, TEMPLATE_PATH, jinja2_view
import requests

TEMPLATE_PATH[:] = ['templates']

values = {'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound'
                }

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


@route('/', name='home', method='GET')
@jinja2_view('index.html')
def index():
    return {'title':'Home',
            'values':values}

@get('/index')
def select():
    return '''
    <form action="/convert" method="post">
            <p>Convert From:<select name="convert_from">
            <option value="USD">US Dollar</option>
            <option value="EUR">Euro</option>
            <option value="GBP">British Pound</option>
            </select>
            </p>
            <p>Convert To:  <select name="convert_to">
            <option value="EUR">Euro</option>
            <option value="USD">US Dollar</option>
            <option value="GBP">British Pound</option>
            </select>
            </p>
            <p>Value to convert: <input name="value_to_convert" type="float" /></p>
        <input value="Convert" type="submit" />
	</form>
	'''

@post('/convert')
def convert():
    convert_from = request.forms.get('convert_from').upper()
    convert_to = request.forms.get('convert_to').upper()
    value_to_convert = request.forms.get('value_to_convert')
    url = ('http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=1') % (convert_from, convert_to)
    rate = requests.get(url).json()['v']
    converted = float(value_to_convert)*float(requests.get(url).json()['v'])

    return '''<p>Current exchange rate %s to %s is: <b>%s</b></p>
        <p>Exchange value is: <b>%s</b></p>''' % (convert_from, convert_to, rate, converted)

@route('/result', method='POST')
@jinja2_view('result.html')
def result():
    convert_from = request.forms.get('convert_from').upper()
    convert_to = request.forms.get('convert_to').upper()
    value_to_convert = request.forms.get('value_to_convert')
    url = ('http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=1') % (convert_from, convert_to)
    rate = requests.get(url).json()['v']
    converted = float(value_to_convert)*float(requests.get(url).json()['v'])

    return {'rate':rate,
            'converted':converted,
            'title':'Result'}        

run(host='localhost', port=8080, debug=True)
