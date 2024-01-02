site_configuration = {
    'systems': [
        {
            'name': 'MyLaptop',
            'descr': 'Loal tests on my laptop',
            'hostnames': ['DLHRT0023'],
            # 'modules_system': 'tmod32',
            'partitions': [
                {
                    'name': 'Local_NoMPI_MultiThread',
                    'descr': 'Local cpu without MPI',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'features': ['omp_only'],
                    'max_jobs': 1,
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 12,
                        'num_cpus_per_core': 2,
                        'num_cpus_per_socket': 1,
                        'num_sockets': 1,
                    }
                },
                {
                    'name': 'Local_MPI_SingleThread',
                    'descr': 'Local cpu with MPI',
                    'scheduler': 'local',
                    'launcher': 'mpirun',
                    'features': ['mpi_only'],
                    'max_jobs': 1,
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 12,
                        'num_cpus_per_core': 2,
                        'num_cpus_per_socket': 12,
                        'num_sockets': 1,
                    }
                },
            ]
        }
    ]
}
