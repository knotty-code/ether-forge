#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from network_builder.api.v1alpha1.pysrc.circuitgeniestate import CIRCUITGENIESTATE_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA, SubnetLibrary

# Direct import of the SRL handler so we can pass extra parameters
from network_builder.intents.circuitgenie.srl import SrlBaseConfigHandler

# Keep the factory if you ever need SR OS support
from network_builder.intents.circuitgenie.handlers import get_config_handler

from network_builder.intents.circuitgenie.init import init_globals_defaults, validate


def int_to_ip(ip_int: int) -> str:
    """Convert integer IP to dotted string."""
    return f"{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}"


def parse_port(port_str: str) -> tuple[str, str]:
    """Parse 'node-interface' (e.g. 'leaf1-ethernet-1-8') to (node, interface) with SRL format 'ethernet-1/8'."""
    parts = port_str.split('-', 1)
    if len(parts) != 2:
        raise e.InvalidInput(f"Invalid port format: '{port_str}'. Expected 'node-interface'.")

    node = parts[0]
    # parts[1] is the interface part, e.g. "ethernet-1-8"
    interface_parts = parts[1].split('-', 2)  # Split into at most 3 parts: base, slot, port
    if len(interface_parts) != 3:
        raise e.InvalidInput(
            f"Interface part must be in format 'ethernet-<slot>-<port>', got '{parts[1]}'"
        )

    # Reconstruct as ethernet-<slot>/<port>
    formatted_interface = f"{interface_parts[0]}-{interface_parts[1]}/{interface_parts[2]}"
    return node, formatted_interface


def process_cr(cr):
    """Process CircuitGenie CR - derive nodes/interfaces/IPs and configure via handlers."""
    log_msg("CircuitGenie CR:", dict=cr)
    cr_obj = CircuitGenie.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    ns = cr_obj.metadata.namespace
    validate(cr_obj)
    init_globals_defaults(cr_obj)

    # Parse ports
    if not cr_obj.spec.portA or not cr_obj.spec.portB:
        raise e.InvalidInput("spec.portA and spec.portB are required")

    nodeA, interfaceA = parse_port(cr_obj.spec.portA[0])
    nodeB, interfaceB = parse_port(cr_obj.spec.portB[0])

    log_msg(f"Parsed: nodeA='{nodeA}', interfaceA='{interfaceA}'")
    log_msg(f"Parsed: nodeB='{nodeB}', interfaceB='{interfaceB}'")

    # Supernet selection
    if not cr_obj.spec.supernet or len(cr_obj.spec.supernet) == 0:
        raise e.InvalidInput("spec.supernet is required")

    selected_supernet = cr_obj.spec.supernet[0]
    log_msg(f"User selected supernet: '{selected_supernet}'")

    # Find matching subnets
    all_subnet_crs = eda.list_crs(schema=SUBNETLIBRARY_SCHEMA, filter=[], ns=ns)
    matching_subnets = []
    for subnet_cr_dict in all_subnet_crs:
        subnet_obj = SubnetLibrary.from_input(subnet_cr_dict)
        if subnet_obj and getattr(subnet_obj.spec, "supernet", None) == selected_supernet:
            cidr = f"{subnet_obj.spec.subnet}/{subnet_obj.spec.subnetLength}"
            matching_subnets.append(subnet_obj)
            log_msg(f"MATCH: SubnetLibrary '{subnet_obj.metadata.name}' -> {cidr}")

    if not matching_subnets:
        raise e.InvalidInput(f"No available subnets for supernet '{selected_supernet}'")

    log_msg(f"Found {len(matching_subnets)} matching subnet(s)")

    # Allocate IPs from first subnet
    first_subnet = matching_subnets[0]
    base_ip = first_subnet.spec.subnet
    prefix = first_subnet.spec.subnetLength

    if prefix != 30:
        raise e.InvalidInput(f"Only /30 subnets supported for now (got /{prefix})")

    octets = list(map(int, base_ip.split('.')))
    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

    portA_ip = int_to_ip(ip_int + 1) + f"/{prefix}"
    portB_ip = int_to_ip(ip_int + 2) + f"/{prefix}"

    log_msg(f"Assigned IPs from {base_ip}/{prefix}: portAIP={portA_ip}, portBIP={portB_ip}")

    # Load node CRs
    nodeA_cr = nutils.get_node(name=nodeA)
    nodeB_cr = nutils.get_node(name=nodeB)
    if nodeA_cr is None:
        raise e.InvalidInput(f"Node '{nodeA}' not found")
    if nodeB_cr is None:
        raise e.InvalidInput(f"Node '{nodeB}' not found")

    log_msg(f"Loaded node CR for '{nodeA}'")
    log_msg(f"Loaded node CR for '{nodeB}'")

    # Validate intended outputs
    log_msg("Validating outputs for srl.py handler:")
    log_msg(f"nodeA: {nodeA}, interfaceA: {interfaceA}, portA_ip: {portA_ip}")
    log_msg(f"nodeB: {nodeB}, interfaceB: {interfaceB}, portB_ip: {portB_ip}")

    # === Configure node A ===
    os_a = nodeA_cr["spec"].get("operatingSystem")
    if os_a == PLATFORM_SRL:
        handler_a = SrlBaseConfigHandler()
        handler_a.handle_cr(
            cr_obj=cr_obj,
            node_cr=nodeA_cr,
            interface=interfaceA,
            ip_prefix=portA_ip
        )
        log_msg(f"Handled config for node '{nodeA}' (SRL) with interface {interfaceA} and IP {portA_ip}")
    elif os_a == PLATFORM_SROS:
        handler = get_config_handler(PLATFORM_SROS)
        if handler:
            handler.handle_cr(cr_obj, nodeA_cr)
        else:
            raise e.InvalidInput("No SR OS handler available")
    else:
        raise e.InvalidInput(f"Unsupported OS '{os_a}' on node '{nodeA}'")

    # === Configure node B ===
    os_b = nodeB_cr["spec"].get("operatingSystem")
    if os_b == PLATFORM_SRL:
        handler_b = SrlBaseConfigHandler()
        handler_b.handle_cr(
            cr_obj=cr_obj,
            node_cr=nodeB_cr,
            interface=interfaceB,
            ip_prefix=portB_ip
        )
        log_msg(f"Handled config for node '{nodeB}' (SRL) with interface {interfaceB} and IP {portB_ip}")
    elif os_b == PLATFORM_SROS:
        handler = get_config_handler(PLATFORM_SROS)
        if handler:
            handler.handle_cr(cr_obj, nodeB_cr)
        else:
            raise e.InvalidInput("No SR OS handler available")
    else:
        raise e.InvalidInput(f"Unsupported OS '{os_b}' on node '{nodeB}'")

    # Update state CR
    eda.update_cr(
        schema=CIRCUITGENIESTATE_SCHEMA,
        name=cr_name,
        spec={"nodes": [nodeA, nodeB]}
    )
    log_msg("CircuitGenieState updated with nodes")