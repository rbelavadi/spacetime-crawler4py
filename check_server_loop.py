import socket
import time

def check_cache_server(host="styx.ics.uci.edu", port=9000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)  # 5 second timeout
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

if __name__ == "__main__":
    while True:
        is_up = check_cache_server()
        if is_up:
            print("✅✅✅ CACHE SERVER IS UP! YOU CAN START CRAWLER! ✅✅✅")
            break
        else:
            print("❌ Cache server still down... checking again in 2 minutes...")
        time.sleep(120)  # wait 2 minutes
