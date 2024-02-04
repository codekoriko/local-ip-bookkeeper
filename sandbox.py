from local_ip_bookkeeper.tracker import IPTracker


ip_tracker = IPTracker(
    'MSI Salticidae',
    '5df4f367d185e866235dc6e012761c3f',
    'info.json',
)
ip_tracker.update_ip()
ip_tracker.print_registery()
