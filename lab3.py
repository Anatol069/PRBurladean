import dns.resolver
import socket


def resolve_domain(domain, dns_server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]

        answers = resolver.resolve(domain, "A")
        print(f"Domeniul {domain} are următoarele IP-uri:")
        for rdata in answers:
            print(rdata.to_text())
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
        print(
            f"Eroare: Nu s-a găsit niciun răspuns pentru domeniul {domain}. Detalii: {e}"
        )
    except Exception as e:
        print(f"Eroare generală: {e}")


def resolve_ip(ip, dns_server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]

        socket.inet_aton(ip)

        reversed_ip = ".".join(reversed(ip.split("."))) + ".in-addr.arpa"
        answers = resolver.resolve(reversed_ip, "PTR")
        print(f"IP-ul {ip} este asociat cu domeniile:")
        for rdata in answers:
            print(rdata.to_text())
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
        print(f"Eroare: Nu s-au găsit domenii pentru IP-ul {ip}. Detalii: {e}")
    except socket.error:
        print(f"Eroare: Adresa IP {ip} nu este validă.")
    except Exception as e:
        print(f"Eroare generală: {e}")


def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def main():
    dns_server = "1.1.1.1"
    print(f"Folosind serverul DNS: {dns_server}")

    while True:
        command = input("Introduceți comanda: ").strip()

        if command.startswith("resolve"):
            parts = command.split()
            if len(parts) == 2:
                if is_valid_ip(parts[1]):
                    resolve_ip(parts[1], dns_server)
                else:
                    resolve_domain(parts[1], dns_server)
            else:
                print("Comandă invalidă! Folosiți: resolve <domain> sau resolve <ip>")

        elif command.startswith("use dns"):
            parts = command.split()
            if len(parts) == 3:
                try:
                    if is_valid_ip(parts[2]):
                        dns_server = parts[2]
                        print(f"Server DNS schimbat la: {dns_server}")
                    else:
                        print("Eroare: Adresa IP a serverului DNS este invalidă.")
                except socket.error:
                    print("Eroare: Adresa IP a serverului DNS este invalidă.")
            else:
                print("Comandă invalidă! Folosiți: use dns <ip>")

        elif command.lower() == "exit":
            print("Ieșire din aplicație.")
            break


if __name__ == "__main__":
    main()
