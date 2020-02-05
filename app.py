import socket
import geoip2.database
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

geodb = geoip2.database.Reader('geolite2-city.mmdb')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        abort(400, {'message': 'Please use GET to access this endpoint'})
    else:
        client_ip = request.remote_addr
        host_name = socket.gethostname()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = {
            'host_name': host_name,
            'your_ip': client_ip,
            'datetime': current_time
        }

        try:
            geo_response = geodb.city(str(request.remote_addr))
            client_country = geo_response.country.name
            client_postal = geo_response.postal.code
            client_city = geo_response.city.name
            client_lat = geo_response.location.latitude
            client_lng = geo_response.location.longitude
        except Exception as e:
            print('[INFO] Unable to decode ip address {} ({})'.format(
                client_ip, e.args))
            result['status'] = '201'
            return jsonify({
                'client': result
            })

        result['status'] = '200'
        result['your_country'] = client_country
        result['your_city'] = client_city
        result['your_post_code'] = client_postal
        result['your_latitude'] = client_lat
        result['your_longitude'] = client_lng

        return jsonify({
            'client': result
        }), 200


if __name__ == '__main__':
    app.run(debug=False)
