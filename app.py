#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os

from models import *

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

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Wine).order_by(Wine.title).paginate(
        page=1, per_page=9)
    return render_template('index.html', pagination=pagination, count = len(pagination.items))

#page for filters
@app.route('/filter')
def filtered_page_for_country():

    #examples for routes to call
    #/filter?country=Italy
    #/filter?country=Italy+USA
    #/filter?country=Italy&variety=Syrah

    #get filter parameters from URL
    country_filter = request.args.get('country')
    variety_filter = request.args.get('variety')
    primary_filter = request.args.get('primaries')
    secundary_filter = request.args.get('secundaries')
    tertiary_filter = request.args.get('tertiaries')


    #filtering
    data = db.session.query(Wine)
    
    if country_filter is not None:
        data = data.filter(Wine.country == country_filter)
    if variety_filter is not None:
        data = data.filter(Wine.variety == variety_filter)
    """
    if country_filter is not None:
        data = data.filter(Wine.country == country_filter)
    if country_filter is not None:
        data = data.filter(Wine.country == country_filter)
    if country_filter is not None:
        data = data.filter(Wine.country == country_filter)
    """
        
    data = data.order_by(Wine.title)

    #pagination
    page = request.args.get('page', 1, type=int)
    pagination = data.paginate(page=1, per_page=9)
    return render_template('filter.html', 
                           pagination=pagination, 
                           count = len(pagination.items),  
                           filter_1 = country_filter, 
                           filter_2 = variety_filter)



### search endpoint
@app.route('/search') 
def search():
    query = request.args.get('search') 
    req_search = db.session.query(Wine).filter_by(id=query) ### filter on multiple fields
    return render_template('search.html', req_search=req_search)

@app.route('/wine/<int:id>')
def wine(id):
    "Takes an id, return product page"
    wine = db.session.query(Wine).get(id)
    wine_d = wine.to_dict()
    return render_template('product.html', wine=wine_d)


@app.route('/wine/list/<int:limit>')
def wine_list(limit):
    "Takes a limit, return a list of wines"
    wines = db.session.query(Wine).limit(limit).all()
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
