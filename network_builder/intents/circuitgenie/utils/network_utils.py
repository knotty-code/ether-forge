#!/usr/bin/env python3
import utils.exceptions as e


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