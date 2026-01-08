from utils.log import log_msg
import utils.exceptions as e

def expand_port_ranges(port_selector: str) -> list[str]:
    """Expand '1-5,7-10,12' into ['1', '2', '3', '4', '5', '7', '8', '9', '10', '12']"""
    if not port_selector:
        return []

    ports = set()
    for part in port_selector.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start, end = part.split('-', 1)
            try:
                start_int = int(start.strip())
                end_int = int(end.strip())
                if start_int <= end_int:
                    ports.update(str(i) for i in range(start_int, end_int + 1))
                else:
                    log_msg(f"Invalid range (start > end): {part}")
            except ValueError:
                log_msg(f"Invalid range format: {part}")
        else:
            try:
                ports.add(str(int(part)))
            except ValueError:
                log_msg(f"Invalid single port: {part}")

    return sorted(ports)

def int_to_ip(ip_int: int) -> str:
    """Convert integer IP to dotted string.  
    Because someone thought storing IPs as integers was a good idea."""
    return f"{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}"


def parse_port(port_str: str) -> tuple[str, str]:
    """Parse 'node-interface' string into (node, SRL-formatted interface).  
    Because 'leaf1-ethernet-1-8' is apparently too straightforward."""
    parts = port_str.split('-', 1)
    if len(parts) != 2:
        raise e.InvalidInput(f"Invalid port format: '{port_str}'. Did you even read the docs?")

    node = parts[0]
    interface_parts = parts[1].split('-', 2)
    if len(interface_parts) != 3:
        raise e.InvalidInput(
            f"Interface must be 'ethernet-<slot>-<port>', got '{parts[1]}'. "
            "Congratulations, you broke basic string parsing."
        )

    formatted_interface = f"{interface_parts[0]}-{interface_parts[1]}/{interface_parts[2]}"
    return node, formatted_interface