import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init()

PORTS = [
    21, 22, 23, 25, 53, 69, 80, 81, 110, 135, 139, 143, 443, 445, 554, 587, 993, 995,
    512, 513, 514, 7070, 9100, 1433, 1723, 3306, 3389, 4444, 5000, 5353, 5900, 8000,
    8080, 8443, 8888, 6666, 5555, 37777, 2323, 1099, 2000, 31337
]

TIMEOUT = 1.0
open_ports_dict = {}

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((str(ip), port))
            if result == 0:
                print(f"{Fore.GREEN}[+] {ip}:{port} открыт{Style.RESET_ALL}")
                if ip not in open_ports_dict:
                    open_ports_dict[ip] = []
                open_ports_dict[ip].append(port)
            else:
                print(f"{Fore.YELLOW}[-] {ip}:{port} закрыт{Style.RESET_ALL}")
    except Exception:
        pass

def scan_ip(ip):
    for port in PORTS:
        scan_port(ip, port)

def scan_network(cidr_range, threads=100):
    print(f"{Fore.CYAN}Начинаем сканирование сети {cidr_range}...{Style.RESET_ALL}")
    ip_net = ipaddress.ip_network(cidr_range, strict=False)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for ip in ip_net.hosts():
            executor.submit(scan_ip, ip)

    # Печать открытых портов
    print(f"\n{Fore.MAGENTA}Открытые порты по IP:{Style.RESET_ALL}")
    for ip, ports in open_ports_dict.items():
        print(f"{Fore.GREEN}{ip}:{Style.RESET_ALL} {', '.join(map(str, ports))}")

if __name__ == "__main__":
    target_network = input("Введите подсеть (например 192.168.1.0/24): ")
    scan_network(target_network)
