#!/usr/bin/env python3
# generic_debug_state.py
# Generic state script to explore ANY state DB path
# Just change target_path below!

from utils.log import log_msg
import eda_state as estate

# CHANGE THIS LINE TO WHATEVER PATH YOU WANT TO EXPLORE
target_path = ".namespace.resources.cr.network-builder_eda_local.v1alpha1.circuitgeniestate"

def process_state_cr(cr):
    log_msg("Generic Debug State Intent Starting")
    log_msg("Input CR", dict=cr)
    log_msg(f"Target Path: {target_path}")

    entries = []
    try:
        for row in estate.list_db(path=target_path, fields=[]):
            path = row.get("path", "")
            value = row.get("value", {})

            # Try to extract resource name from path (works for most CRs and normalized paths)
            resource_name = "unknown"
            name_parts = [p for p in path.split('.') if '{.name=="' in p]
            if name_parts:
                resource_name = name_parts[-1].split('{.name=="')[1].split('"')[0]

            entries.append({
                "name": resource_name,
                "full_path": path,
                "value": value
            })
    except Exception as e:
        log_msg("Error during list_db query", dict={"error": str(e)})

    log_msg(f"Found {len(entries)} entries matching the path")

    # Sort for consistent output
    entries.sort(key=lambda x: x["name"])

    # Pretty dump
    for i, entry in enumerate(entries, 1):
        log_msg(f"--- Entry #{i}: {entry['name']} ---")
        log_msg("Full Path", dict={"path": entry["full_path"]})
        if entry["value"]:
            log_msg("Value", dict=entry["value"])
        else:
            log_msg("Value: <empty>")
        log_msg("---")

    log_msg("Generic Debug Complete")