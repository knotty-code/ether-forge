from utils.log import log_msg


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