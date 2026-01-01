from common.constants import PLATFORM_SRL, PLATFORM_SROS
import utils.exceptions as e
# Handlers — because apparently we still support multiple platforms in 2026
from network_builder.intents.circuitgenie.srl import SrlBaseConfigHandler
from network_builder.intents.circuitgenie.handlers import get_config_handler
from utils.log import log_msg

def configure_node(cr_obj, node_name: str, node_cr: dict, interface: str, ip_prefix: str = None):
    """Configure a single node. Now with proper dependency injection."""
    os = node_cr["spec"].get("operatingSystem")
    if os == PLATFORM_SRL:
        handler = SrlBaseConfigHandler()
        handler.handle_cr(cr_obj=cr_obj, node_cr=node_cr, interface=interface, ip_prefix=ip_prefix)
        log_msg(f"Successfully tormented SRL node '{node_name}' with interface {interface} and IP {ip_prefix}")
    elif os == PLATFORM_SROS:
        handler = get_config_handler(PLATFORM_SROS)
        if handler:
            handler.handle_cr(cr_obj, node_cr)  # SR OS might not need cr_obj — check later
            log_msg(f"SR OS node '{node_name}' configured. Miracles do happen.")
        else:
            raise e.InvalidInput("SR OS handler missing. Someone forgot to implement it.")
    else:
        raise e.InvalidInput(f"Unsupported OS '{os}' on node '{node_name}'. What is this, 2010?")