import socket

def server(frames, window_size):
    server_address = ('localhost', 10000)
    print('Starting server on {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    try:
        base = 0
        while base < frames:
            frames_received = set()
            while len(frames_received) < window_size:
                data, address = sock.recvfrom(1024)
                frame_number = int(data.decode())
                print(f'Received frame {frame_number}')
                frames_received.add(frame_number)
            ack = min(frames_received)
            print(f'Sending ACK for frame {ack}')
            sock.sendto(str(ack).encode(), address)
            base = ack + 1
    finally:
        print('Closing socket')
        sock.close()

if __name__ == "__main__":
    total_frames = int(input("Enter total number of frames: "))
    window_size = int(input("Enter window size: "))

    server(total_frames, window_size)
