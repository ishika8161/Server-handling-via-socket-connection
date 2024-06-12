import socket
import random
import time

def client(frames, window_size, lost_packets):
    server_address = ('localhost', 10000)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        frame_number = 0
        base = 0
        while base < frames:
            for i in range(base, min(base + window_size, frames)):
                if i not in lost_packets:
                    print(f'Sending frame {i}')
                    sock.sendto(str(i).encode(), server_address)
                    time.sleep(0.1)  # Simulating transmission delay
            try:
                sock.settimeout(1)  # Setting timeout for receiving ack
                while True:
                    ack, _ = sock.recvfrom(1024)
                    ack = int(ack.decode())
                    print(f'Received ACK for frame {ack}')
                    if ack == base:
                        base += 1
                        break
            except socket.timeout:
                print('Timeout, resending frames...')
                continue
            finally:
                sock.settimeout(None)  # Resetting timeout
    finally:
        print('Closing socket')
        sock.close()

if __name__ == "__main__":
    total_frames = int(input("Enter total number of frames: "))
    window_size = int(input("Enter window size: "))
    lost_packets = [int(x) for x in input("Enter lost packet numbers separated by commas: ").split(',')]

    client(total_frames, window_size, lost_packets)
