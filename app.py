from flask import Flask, jsonify, render_template, request
from database import db_session
from models import find_closest_stache
import os

# initialization
app = Flask(__name__)
app.config.update(DEBUG=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def map():
    """Renders the home page of BikeStache."""
    return render_template('stachemap.html')


@app.route('/get_stache', methods=['POST'])
def get_stache():
    """REST API for returning the nearest bikestache.
    Expects a POST with the latitude and longitude of the user.
    """
    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lng = float(request.form['longitude'])
        if _valid_coordinates(lat, lng):
            stache = find_closest_stache(lat, lng)
            if stache:
                return jsonify({'status_code': 200,
                                'message': 'Success',
                                'stache': stache.as_dict()})
            return jsonify({'status_code': 200,
                            'message': 'No stache within {0} miles'.format(5),
                            'stache': None})
        raise InvalidUsage('Invalid coordinates.')


def _valid_coordinates(lat, lng):
    """validates latitude and longitude"""
    if lat >= 0 and lat <= 180 and lng >= -180 and lng <= 180:
        return True


class InvalidUsage(Exception):
    """Extends Exception class to include message and optional payload"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(e):
    """Redirect page for 404s"""
    return render_template('404.html'), 404

# launch
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
