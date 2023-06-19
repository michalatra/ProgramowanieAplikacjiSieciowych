import ipaddress


def validate_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    ip = input("Podaj Adres IP: ")

    if validate_ip(ip):
        print("Valid IP address.")
    else:
        print("INVALID IP address.")