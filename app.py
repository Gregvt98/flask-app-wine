#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os

import models
import random
import itertools

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Custom routes.
#----------------------------------------------------------------------------#

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ontology')
def ontology():
    return render_template('ontology.html')

@app.route('/')
@app.route('/index')
def index():

    #page filters
    list_of_countries = ['US', 'France', 'Italy', 'Spain', 'Argentina', 'Australia', 'Canada']
    list_of_varieties = ['Pinot Noir', 'Chardonnay', 'Red Blend', 'Cabernet Sauvignon', 'Sangiovese', 'Syrah', 'Rose', 'Riesling', 'Malbec', 'Nebbiolo', 'Sauvignon Blanc', 'Tempranillo', 'Sparkling Blend', 'White Blend']
    list_of_primaries = ['Earth','Vegetable','Spice','Noble Rot','Dried Fruit','Black Fruit','Red Fruit','Tropical Fruit','Tree Fruit','Citrus','Flower']
    list_of_secondaries = ['Microbial']
    list_of_tertiaries = ['Oak Aging', 'General Aging']

    #random values for randomized search result
    random_country = random.choice(list_of_countries)
    random_variety = random.choice(list_of_varieties)
    random_primary = random.choice(list_of_primaries)
    random_secondary = random.choice(list_of_secondaries)
    random_tertiary = random.choice(list_of_tertiaries)

    #pagination
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(models.Wine).order_by(models.Wine.title).paginate(
        page=1, per_page=9)

    return render_template('index.html', 
                           pagination=pagination, 
                           count = len(pagination.items),
                           random_country = random_country,
                           random_variety = random_variety,
                           random_primary = random_primary,
                           random_secondary = random_secondary,
                           random_tertiary = random_tertiary)

#page for filters
@app.route('/filter')
def filter_page():

    #examples for routes to call
    #/filter?country=Italy
    #/filter?country=Italy+USA
    #/filter?country=Italy&variety=Syrah


    #page filters
    list_of_countries = ['US', 'France', 'Italy', 'Spain', 'Argentina', 'Australia', 'Canada']
    list_of_varieties = ['Pinot Noir', 'Chardonnay', 'Red Blend', 'Cabernet Sauvignon', 'Sangiovese', 'Syrah', 'Rose', 'Riesling', 'Malbec', 'Nebbiolo', 'Sauvignon Blanc', 'Tempranillo', 'Sparkling Blend', 'White Blend']
    list_of_primaries = ['Earth','Vegetable','Spice','Noble Rot','Dried Fruit','Black Fruit','Red Fruit','Tropical Fruit','Tree Fruit','Citrus','Flower']
    list_of_secondaries = ['Microbial']
    list_of_tertiaries = ['Oak Aging', 'General Aging']

    #get filter parameters from URL
    country_filter = request.args.getlist('country')
    variety_filter = request.args.getlist('variety')
    primary_filter = request.args.getlist('primary')
    secondary_filter = request.args.getlist('secondary')
    tertiary_filter = request.args.getlist('tertiary')

    #filtering
    data = db.session.query(models.Wine)
    
    if country_filter:
        data = data.filter(models.Wine.country.in_(country_filter))
    if variety_filter:
        data = data.filter(models.Wine.variety.in_(variety_filter))
    
    #Filtering for .getlist object is different because you need to check if there is an empty list or not.
    if primary_filter:
        for f in primary_filter:
            data = data.filter(models.Wine.primary_flavor.contains(f))
    
    if secondary_filter:
        for f in secondary_filter:
            data = data.filter(models.Wine.secondary_flavor.contains(f))

    if tertiary_filter:
        for f in tertiary_filter:
            data = data.filter(models.Wine.tertiary_flavor.contains(f))


    data = data.order_by(models.Wine.title)

    #pagination
    page = request.args.get('page', 1, type=int)
    pagination = data.paginate(page=1, per_page=9)

    #remove Nonetypes
    if country_filter is None:
        country_filter = ['0']

    if variety_filter is None:
        variety_filter = ['0']

    if primary_filter is None:
        primary_filter = ['0']

    if secondary_filter is None:
        secondary_filter = ['0']

    if tertiary_filter is None:
        tertiary_filter = ['0']
        

    #return template with variables
    return render_template('filter.html', 
                           pagination=pagination, 
                           count = len(pagination.items), 
                           list_of_countries = list_of_countries,
                           list_of_varieties = list_of_varieties,
                           list_of_primaries = list_of_primaries, 
                           list_of_secondaries = list_of_secondaries,
                           list_of_tertiaries = list_of_tertiaries,
                           country_filter = country_filter, 
                           variety_filter = variety_filter,
                           primary_filter = primary_filter,
                           secondary_filter = secondary_filter,
                           tertiary_filter = tertiary_filter
                           )



### search endpoint
@app.route('/search') 
def search():
    query = request.args.get('search') 
    req_search = db.session.query(models.Wine).filter_by(id=query) ### filter on multiple fields
    return render_template('search.html', req_search=req_search) 

@app.route('/wine/<int:id>')
def get_wine(id):
    "Takes an id, return product page"
    entry = db.session.query(models.Wine).get(id)
    wine_d = entry.to_dict()
    #return jsonify(wine_d)
    return render_template('product.html', result=wine_d)


@app.route('/wine/list/<int:limit>')
def wine_list(limit):
    "Takes a limit, return a list of wines"
    wines = db.session.query(models.Wine).limit(limit).all()
    results = [w.to_dict() for w in wines]
    return jsonify(results)

"""

@app.route('/paginated_results')
def wines():
 ROWS_PER_PAGE = 5
 page = request.args.get('page', 1, type = int)
 
 wines = db.session.query(Wine).paginate(page = page, per_page = ROWS_PER_PAGE)
 paginated_wines =(wines.items)
 
 results = [{
   'id':wine.id,
   'title':wine.title,
   'description':wine.description
 } for wine in paginated_wines]
 
 return jsonify({
   'success':True,
   'results':results,
   'count':len(paginated_wines)
 })

"""




#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
