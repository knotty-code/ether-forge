#!/usr/bin/env python3
from utils.log import log_msg
import utils.exceptions as e
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from network_builder.api.v1alpha1.pysrc.circuitgeniestate import CIRCUITGENIESTATE_SCHEMA
from network_builder.intents.circuitgenie.utils.network_utils import parse_port, int_to_ip
from network_builder.intents.circuitgenie.utils.config_node import configure_node



class CircuitConfigOrchestrator:
    """Orchestrates the full CircuitGenie configuration flow.  
    Because chaos is only fun in logs, not in code."""
    def _error(self, msg: str):
            """Raise a properly contextualized tantrum. Because context matters."""
            raise e.InvalidInput(f"[CircuitGenie '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: CircuitGenie):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        """Main orchestration — the new process_cr."""
        log_msg(f"Orchestrator awakened for CR '{self.cr_name}'. Let the games begin.")
        
        ports = self._parse_ports()
        supernet = self._validate_supernet()
        subnets = self._find_matching_subnets(supernet)
        ips = self._allocate_ips(subnets[0])  # Take first available
        nodes = self._load_nodes(ports)
        self._configure_endpoints(nodes, ports, ips)
        self._update_state(nodes)

        log_msg(f"Orchestrator complete for '{self.cr_name}'. Another flawless victory.")

    def _parse_ports(self):
        """Parse portA/portB with maximum judgment."""
        if not self.cr_obj.spec.portA or not self.cr_obj.spec.portB:
            self._error("portA and portB are required. This is not rocket surgery.")

        node_a, intf_a = parse_port(self.cr_obj.spec.portA[0])
        node_b, intf_b = parse_port(self.cr_obj.spec.portB[0])
        log_msg(f"Parsed ports: A={node_a}/{intf_a}, B={node_b}/{intf_b}")
        return {"A": (node_a, intf_a), "B": (node_b, intf_b)}

    def _validate_supernet(self):
        """Ensure user provided a supernet. We have standards."""
        if not self.cr_obj.spec.supernet:
            raise e.InvalidInput("spec.supernet required. This isn't optional.")
        supernet = self.cr_obj.spec.supernet[0]
        log_msg(f"User demands supernet '{supernet}'. Bold.")
        return supernet

    def _find_matching_subnets(self, supernet):
        """Hunt down subnets like a network bloodhound."""
        from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA, SubnetLibrary
        import eda_common as eda

        all_subnets = eda.list_crs(schema=SUBNETLIBRARY_SCHEMA, filter=[], ns=self.ns)
        matches = []
        for subnet_cr in all_subnets:
            subnet = SubnetLibrary.from_input(subnet_cr)
            if subnet and getattr(subnet.spec, "supernet", None) == supernet:
                cidr = f"{subnet.spec.subnet}/{subnet.spec.subnetLength}"
                matches.append(subnet)
                log_msg(f"Match found: '{subnet.metadata.name}' -> {cidr}")

        if not matches:
            raise e.InvalidInput(f"No subnets for supernet '{supernet}'. You're out of luck.")
        log_msg(f"Found {len(matches)} subnets. Plenty to work with.")
        return matches

    def _allocate_ips(self, subnet):
        """Allocate /30 IPs. Only /30. We have rules."""
        if subnet.spec.subnetLength != 30:
            raise e.InvalidInput(f"Only /30 supported. Got /{subnet.spec.subnetLength}. Rebel.")
        
        base_ip = subnet.spec.subnet
        octets = list(map(int, base_ip.split('.')))
        ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
        
        ip_a = int_to_ip(ip_int + 1) + "/30"
        ip_b = int_to_ip(ip_int + 2) + "/30"
        log_msg(f"Allocated: A={ip_a}, B={ip_b}. Efficient as always.")
        return {"A": ip_a, "B": ip_b}

    def _load_nodes(self, ports):
        """Kidnap node CRs."""
        import utils.node_utils as nutils
        node_a, _ = ports["A"]
        node_b, _ = ports["B"]
        cr_a = nutils.get_node(name=node_a)
        cr_b = nutils.get_node(name=node_b)
        if not cr_a or not cr_b:
            raise e.InvalidInput(f"Node missing: A={node_a}, B={node_b}. Did someone delete reality?")
        log_msg(f"Nodes acquired: {node_a}, {node_b}")
        return {"A": (node_a, cr_a), "B": (node_b, cr_b)}

    def _configure_endpoints(self, nodes, ports, ips):
        """Inflict configuration upon the endpoints."""
        log_msg("Beginning the sacred ritual of configuration...")
        for endpoint in ["A", "B"]:
            node_name, node_cr = nodes[endpoint]
            _, interface = ports[endpoint]
            ip_prefix = ips[endpoint]
            configure_node(self.cr_obj, node_name, node_cr, interface, ip_prefix)

    def _update_state(self, nodes):
        """Update state CR. The circle is complete."""
        import eda_common as eda
        node_names = [nodes["A"][0], nodes["B"][0]]
        subnets = ["test123"]
        eda.update_cr(
            schema=CIRCUITGENIESTATE_SCHEMA,
            name=self.cr_name,
            spec={
                "nodes": node_names,
                "subnets": subnets
            }
        )
        log_msg("State updated. Users will be so impressed.")