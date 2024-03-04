''' Author - Prathamesh Kandpal (plk7197)'''
from flask import Flask, request, jsonify
import socket
import json
import requests

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return 'Missing parameters', 400

    if not number.isdigit():
        return 'Invalid number', 400

    dns_query = json.dumps({"TYPE": "A", "NAME": hostname})
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(dns_query.encode(), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(1024)
        response = json.loads(data.decode())
    except (socket.timeout, socket.error) as e:
        return jsonify(error=str(e)), 500
    except json.JSONDecodeError:
        return jsonify(error='Invalid JSON response'), 500
    finally:
        sock.close()

    if 'VALUE' in response:
        fs_ip = response['VALUE']
        try:
            fib_response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci?number={number}')
            if fib_response.status_code == 200:
                fib_data = fib_response.json()
                if 'result' in fib_data:
                    return jsonify(fib_number=fib_data['result']), 200
                else:
                    return jsonify(error='Malformed response from Fibonacci Server'), fib_response.status_code
            else:
                return jsonify(error='Failed to calculate Fibonacci number'), fib_response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify(error=str(e)), 500
    else:
        return jsonify(error='DNS query failed or no VALUE in response'), 500

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

