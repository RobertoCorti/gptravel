from flask import Flask, render_template, request, redirect, url_for
import pycountry
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        region = request.form.get('region')

        if region:
            return redirect(url_for('travel_plan',
                                    country=country,
                                    departure_date=departure_date,
                                    return_date=return_date,
                                    region=region))
        else:
            return redirect(url_for('travel_plan',
                                    country=country,
                                    departure_date=departure_date,
                                    return_date=return_date))
    else:
        return render_template('index.html')


@app.route('/travel_plan/<country>/<departure_date>/<return_date>')
@app.route('/travel_plan/<country>/<departure_date>/<return_date>/<region>')
def travel_plan(country, departure_date, return_date, region=None):
    wiki_summary = None
    try:
        country_name = pycountry.countries.get(alpha_2=country).name
    except AttributeError:
        country_name = country
    if region:
        # get region page
        region_page = wiki_wiki.page(region)
        if region_page.exists():
            wiki_summary = region_page.summary
    else:
        # get country page from wikipedia
        country_page = wiki_wiki.page(country_name)

        if country_page.exists():
            wiki_summary = country_page.summary

    if wiki_summary is not None:
        wiki_summary = '.'.join(wiki_summary.split('.')[:3])

    return render_template('travel_plan.html',
                           departure_date=departure_date,
                           return_date=return_date,
                           summary=wiki_summary)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
