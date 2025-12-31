#!/usr/bin/env python3
import eda_common as eda
import eda_state as estate
from utils.log import log_msg

# Import the generated models and constants
from network_builder.api.v1alpha1.pysrc.portlibrarystate import PortLibraryState
from network_builder.api.v1alpha1.pysrc.portlibrary import PORTLIBRARY_SCHEMA  # <-- Use this!

from network_builder.intents.portlibrarystate.state_handlers import get_state_handler
from network_builder.intents.portlibrarystate.init import init_globals_defaults, validate


def process_state_cr(cr):
    log_msg('Processing PortLibraryState CR:', dict=cr)
    cr_obj = PortLibraryState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler('eda')
    handler.handle_cr(cr_obj)

    # Fetch derived PortLibrary CRs
    port_library_crs_iter = eda.list_crs(
        schema=PORTLIBRARY_SCHEMA,  # <-- Cleaner and safer
        ns=cr_obj.metadata.namespace,
        label_filter=['eda.nokia.com/source=derived']
    )

    port_library_crs = list(port_library_crs_iter)
    log_msg(f'Found {len(port_library_crs)} derived PortLibrary CR(s) in namespace {cr_obj.metadata.namespace}')

    # Find matching PortLibrary
    port_library_cr = None
    for candidate in port_library_crs:
        cr_value = candidate.get('value', {})
        candidate_name = cr_value.get('metadata', {}).get('name')
        log_msg('Candidate PortLibrary CR name:', candidate_name)

        if candidate_name == cr_obj.metadata.name:
            port_library_cr = cr_value
            log_msg('Matched PortLibrary CR found!')
            break

    if not port_library_cr:
        log_msg('Could not find matching PortLibrary CR')
        op_state = 'unknown'
    else:
        port_name = port_library_cr.get('spec', {}).get('port')
        nodes = cr_obj.spec.nodes or []

        if not port_name or not nodes:
            op_state = 'unknown'
        else:
            node = nodes[0]
            interface_path = f'.namespace.node{{.name=="{node}"}}.srl.interface{{.name=="{port_name}"}}'
            fields = ['oper-state', 'admin-state']

            try:
                result = next(estate.list_db(path=interface_path, fields=fields))
                value = result.get('value', {})
                op_state = value.get('oper-state', 'unknown')
                log_msg(f'Found {port_name} on {node}: oper-state={op_state}', dict=value)
            except StopIteration:
                log_msg(f'No telemetry data for {port_name} on {node}')
                op_state = 'unknown'

    # Write opstate to the main PortLibrary resource status
    eda.update_cr(
        schema=PORTLIBRARY_SCHEMA,
        name=cr_obj.metadata.name,
        status={
            'opstate': op_state,
            'adminState': value.get('admin-state', 'unknown')
        }
    )
    log_msg('Updated PortLibrary status:', {'opstate': op_state, 'adminState': value.get('admin-state', 'unknown')})
