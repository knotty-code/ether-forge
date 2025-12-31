#!/usr/bin/env python3
import eda_common as eda
import eda_state as estate  # For querying the state DB
from common.constants import PLATFORM_EDA
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.portlibrarystate import PortLibraryState
from network_builder.intents.portlibrarystate.state_handlers import get_state_handler
from network_builder.intents.portlibrarystate.init import init_globals_defaults, validate


def process_state_cr(cr):
    log_msg('PortLibraryState CR:', dict=cr)
    cr_obj = PortLibraryState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(cr_obj)

    # Parse node and interface from CR name (assumes format "node-interface")
    cr_name_parts = cr_obj.metadata.name.split('-', 1)
    if len(cr_name_parts) != 2:
        log_msg('Invalid CR name format; skipping query:', dict=cr_obj.metadata.name)
        op_state = 'unknown'
    else:
        node, interface = cr_name_parts
        # Filtered query for this specific port on this node
        interface_path = f'.namespace.node{{.name=="{node}"}}.srl.interface{{.name=="{interface}"}}'
        fields = ['name', 'admin-state', 'oper-state']
        try:
            interface_data = next(estate.list_db(path=interface_path, fields=fields))
            log_msg(f'Queried interface {interface} on node {node}:', dict=interface_data)
            op_state = interface_data.get('value', {}).get('oper-state', 'unknown')
        except StopIteration:
            log_msg(f'No data found for interface {interface} on node {node}')
            op_state = 'unknown'

    # Update the CR status with OpState
    schema = eda.Schema(group='network-builder.eda.nokia.com', version='v1alpha1', kind='PortLibraryState')  # Adjust if needed
    status = {'opstate': op_state}
    eda.update_cr(schema=schema, name=cr_obj.metadata.name, status=status)
    log_msg('Updated OpState in status:', dict=status)