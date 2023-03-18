from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('travel_plan',
                                country=request.form['country'],
                                departure_date=request.form['departure_date'],
                                return_date=request.form['return_date']))
    else:
        return render_template('base.html')


@app.route('/travel_plan/<country>/<departure_date>/<return_date>')
def travel_plan(country, departure_date, return_date):
    return "Travel plan for region: {}, departure date: {}, return date: {}".format(
        country, departure_date, return_date
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
