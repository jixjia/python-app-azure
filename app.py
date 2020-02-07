import socket
import geoip2.database
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

# Initiate IP decode database
geodb = geoip2.database.Reader('geolite2-city.mmdb')

# Initialize flask app config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Book_of_Architecture'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        abort(400, {'message': 'Please use GET to access this endpoint'})

    else:
        remote_ip = request.environ['REMOTE_ADDR'] if request.environ.get(
            'HTTP_X_FORWARDED_FOR') is None else request.environ['HTTP_X_FORWARDED_FOR']
        client_ip = remote_ip.split(':')[0]
        host_name = socket.gethostname()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output = []
        result = {
            'host_name': host_name,
            'your_ip': client_ip,
            'datetime': current_time
        }

        try:
            geo_response = geodb.city(str(client_ip))
            client_country = geo_response.country.name
            client_postal = geo_response.postal.code
            client_city = geo_response.city.name
            client_lat = geo_response.location.latitude
            client_lng = geo_response.location.longitude
            result['status'] = '200'
            result['your_country'] = client_country
            result['your_city'] = client_city
            result['your_post_code'] = client_postal
            result['your_latitude'] = client_lat
            result['your_longitude'] = client_lng

        except Exception as e:
            result['error_msg'] = 'Unable to decode ip address ({})'.format(
                e.args)
            result['status'] = '201'

        output.append(result)
        # (1) Render response as JSON
        # return jsonify({
        #     'client': result
        # }), 200

        # (2) Render response as HTML template
        return render_template(
            'index.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)
