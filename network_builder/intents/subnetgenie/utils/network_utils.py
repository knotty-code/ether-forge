import utils.exceptions as e

from utils.ip import get_network_for_address, get_ip_proto_from_address


def subnet_split(cidr: str, new_length: int):
    """Split CIDR into smaller subnets using utils.ip for network address."""
    # Get protocol and normalized network address
    proto = get_ip_proto_from_address(cidr.split('/')[0])
    if proto not in ('ipv4', 'ipv6'):
        raise e.InvalidInput(f"Unsupported or invalid address in subnet: {cidr}")

    net = get_network_for_address(cidr)
    ip_str, prefix_str = net.split('/')
    prefix = int(prefix_str)

    if prefix >= new_length:
        raise e.InvalidInput(f"subnetLength ({new_length}) must be greater than original prefix ({prefix})")

    bit_length = 32 if proto == 'ipv4' else 128
    if new_length > bit_length:
        raise e.InvalidInput(f"subnetLength too large for {proto}")

    subnet_size = 1 << (bit_length - new_length)
    num_subnets = 1 << (new_length - prefix)

    if num_subnets > 1024:
        raise e.InvalidInput(f"Would create too many subnets ({num_subnets}) - adjust input")

    subnets = []

    if proto == 'ipv4':
        octets = list(map(int, ip_str.split('.')))
        ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

        for i in range(num_subnets):
            net_int = ip_int + i * subnet_size
            a = (net_int >> 24) & 255
            b = (net_int >> 16) & 255
            c = (net_int >> 8) & 255
            d = net_int & 255
            subnets.append(f"{a}.{b}.{c}.{d}/{new_length}")

    else:  # ipv6 - not implemented yet
        raise e.InvalidInput("IPv6 subnet subdivision not supported yet")

    return subnets