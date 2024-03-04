'''Author - Prathamesh Kandpal(plk7197)'''
from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    content = request.json
    as_ip = content.get('as_ip', "172.18.0.4")  # Get from JSON or use default
    as_port = content.get('as_port', 53533)  # Get from JSON or use default

    registration_details = json.dumps(content).encode('utf-8')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)  # Set a timeout for socket operations
        sock.sendto(registration_details, (as_ip, as_port))
        response, _ = sock.recvfrom(1024)
        print(f"Response from AS: {response.decode()}")
    except socket.timeout:
        return jsonify(error='Authoritative Server response timed out'), 504
    except socket.error as e:
        return jsonify(error=str(e)), 503
    finally:
        sock.close()  # Make sure to close the socket

    return 'Registered', 201

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')
    if number.isdigit():
        number = int(number)
        result = calculate_fibonacci(number)
        return jsonify(result=result), 200
    else:
        return 'Invalid number', 400

def calculate_fibonacci(n):
    # Fibonacci calculation logic here
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
