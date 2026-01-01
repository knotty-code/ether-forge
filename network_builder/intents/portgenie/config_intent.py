#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e
from utils.log import log_msg

from network_builder.api.v1alpha1.pysrc.portgenie import PortGenie
from network_builder.api.v1alpha1.pysrc.portgeniestate import PORTGENIESTATE_SCHEMA
from network_builder.api.v1alpha1.pysrc.portlibrary import PORTLIBRARY_SCHEMA

from network_builder.intents.portgenie.init import init_globals_defaults, validate


def _expand_port_ranges(port_selector: str) -> list[str]:
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


def process_cr(cr):
    """Process PortGenie CR - create one PortLibrary per selected port on each node."""
    log_msg("PortGenie CR:", dict=cr)
    cr_obj = PortGenie.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)

    nodes = {}

    if cr_obj.spec.nodes is not None and len(cr_obj.spec.nodes) > 0:
        for node in cr_obj.spec.nodes:
            if node not in nodes:
                node_cr = nutils.get_node(name=node)
                if node_cr is None:
                    msg = f"Node {node} not found"
                    raise e.InvalidInput(msg)
                nodes[node] = node_cr

    # Get and expand port ranges
    port_selector = getattr(cr_obj.spec, "portselector", None) or ""
    selected_ports = _expand_port_ranges(port_selector)
    log_msg(f"Port selector '{port_selector}' expanded to: {selected_ports}")

    # Fallback: if no portSelector, use a default set
    if not selected_ports:
        log_msg("No portSelector provided - using default common ports")
        selected_ports = [str(i) for i in range(1, 11)]  # 1-10 as default

    created_count = 0

    for node_name in nodes.keys():
        for port_num in selected_ports:
            intf_name = f"ethernet-1/{port_num}"
            safe_intf = intf_name.replace("/", "-")
            dest_name = f"{node_name}-{safe_intf}"

            log_msg(f"Creating PortLibrary: {dest_name} for {intf_name} on {node_name}")

            eda.update_cr(
                schema=PORTLIBRARY_SCHEMA,
                name=dest_name,
                spec={
                    "nodes": [node_name],
                    "port": intf_name,
                },
            )
            created_count += 1

    log_msg(f"Created {created_count} PortLibrary CRs from selected ports")
