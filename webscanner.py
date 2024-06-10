import requests
import ssl
import socket
import dns.resolver

def check_reachability(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return cert is not None
    except Exception as e:
        return False

def check_dns_settings(domain):
    try:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']  
        answers = resolver.resolve(domain, 'A')
        return [answer.to_text() for answer in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

def check_webpage_content(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        return response.text[:1000]  
    except requests.RequestException as e:
        return ''

def main():
    domain = input("Inserisci il dominio da testare: ")

    is_reachable = check_reachability(domain)
    ssl_valid = check_ssl_certificate(domain)
    dns_records = check_dns_settings(domain)
    page_content = check_webpage_content(domain)

    print(f"\nRisultati del test per il dominio: {domain}")
    print(f"Raggiungibilità: {'Sì' if is_reachable else 'No'}")
    print(f"Certificato SSL valido: {'Sì' if ssl_valid else 'No'}")
    print(f"Record DNS: {dns_records}")
    print(f"Contenuto della pagina web (primi 1000 caratteri): {page_content}")

if __name__ == "__main__":
    main()
