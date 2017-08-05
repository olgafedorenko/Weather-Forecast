from flask import Flask, session, redirect, url_for, escape, request, render_template
from imp import weather
app = Flask(__name__)

@app.route('/hello', methods = ['POST', 'GET'])
def hello():
    print(request.form)
    if request.method == 'POST':
        n_days = int(request.form['n_days'])
        if n_days < 1 or n_days > 5:
            return render_template('hello.html', error_message='N days has to be a value from 1 to 5.')

        return redirect('/current_weather/{}/{}/{}?n_days={}'.format(
            request.form['city_name'],
            request.form['action'],
            request.form['format_temp'],
            n_days,
        ))
    else:
        return render_template('hello.html')

@app.route('/current_weather/<city_name>/<action>/<format_temp>')
def current_weather(city_name=None, action=None, format_temp=None):
    if action == 'today':
        d = weather.current_weather(city_name, format_temp)
        return render_template('dict.html', result=d, current_weather=True)
    elif action == '5d':
        n_days = request.args['n_days']
        ds = weather.week(city_name, format_temp, int(n_days))
        return render_template('dict.html', result=ds, current_weather=False)
    else:
        print('else')
        return 'Action {} not found'.format(action)