'''Author - Prathamesh Kandpal(plk7197)'''
import socket
import json


def main():
    host = '0.0.0.0'  # Bind to all interfaces to be reachable within the Docker network
    port = 53533  # Port for the DNS
    dns_records = {}  # Dictionary to store hostname to IP mappings

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            try:
                request = json.loads(data.decode())

                if request.get('TYPE') == 'A':
                    # It's a DNS query
                    name = request.get('NAME')
                    if name and name in dns_records:
                        ip_address = dns_records[name]
                        response = json.dumps({"TYPE": "A", "NAME": name, "VALUE": ip_address, "TTL": 10})
                        server_socket.sendto(response.encode(), addr)
                    else:
                        server_socket.sendto(json.dumps({'error': 'Not found'}).encode(), addr)
                elif 'hostname' in request and 'ip' in request:
                    # It's a registration
                    dns_records[request['hostname']] = request['ip']
                    server_socket.sendto(json.dumps({'status': 'Registered'}).encode(), addr)
                else:
                    # Handle unexpected JSON format
                    server_socket.sendto(json.dumps({'error': 'Invalid request format'}).encode(), addr)

            except json.JSONDecodeError:
                # Handle invalid JSON
                server_socket.sendto(json.dumps({'error': 'Bad JSON'}).encode(), addr)

        except socket.error as e:
            print(f"Socket error: {e}")


if __name__ == '__main__':
    main()
