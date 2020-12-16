import socket
from struct import unpack_from

UDP_IP = "192.168.15.10"
UDP_PORT = 26761


def parse_buffer(data):
    sensor_names = ["azimuth", "pitch", "roll"]
    sensor_bs = [36, 40, 44]
    return {
        name: unpack_from("!f", data, bs)[0]
        for name, bs in zip(sensor_names, sensor_bs)
    }


def get_data(sock):
    data, addr = sock.recvfrom(1024)
    return parse_buffer(data)


def create_socket(udp_ip=UDP_IP, udp_port=UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    return sock


if __name__ == "__main__":
    sock = create_socket()
    while True:
        print(get_data(sock))
