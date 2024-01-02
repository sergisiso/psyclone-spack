site_configuration = {
    'systems': [
        {
            'name': 'MyLaptop',
            'descr': 'Loal tests on my laptop',
            'hostnames': ['DLHRT0023'],
            # 'modules_system': 'tmod32',
            'partitions': [
                {
                    'name': 'local',
                    'descr': 'single local cpu',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 12,
                        'num_cpus_per_core': 2,
                        'num_cpus_per_socket': 1,
                        'num_sockets': 1,
                    }
                },
            ]
        }
    ]
}
