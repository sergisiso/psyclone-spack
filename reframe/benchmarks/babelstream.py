import os
import sys
import reframe as rfm
import reframe.utility.sanity as sn
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from benchmarks.base import BaseSpackTest


class Babelstream(BaseSpackTest):
    descr = 'Babelstream test using Spack OpenMP version'
    valid_systems = ['+no_mpi']
    executable = 'omp-stream'
    # executable_opts = ['--help']
    mongodb_collection = 'Babelstream'

    @run_after('setup')
    def setup_variables(self):
        cores = int(self.current_partition.processor.num_cpus /
                    self.current_partition.processor.num_cpus_per_core)
        self.env_vars['OMP_NUM_THREADS'] = f'{cores}'
        self.env_vars['OMP_PLACES'] = "cores"

    # Check correctness
    @sanity_function
    def validate_solution(self):
        return sn.assert_found(r'Implementation: OpenMP', self.stdout)

    # Extract performance numbers
    @performance_function('MBytes/sec', perf_key='Copy')
    def extract_copy_perf(self):
        return sn.extractsingle(r'Copy \s+(\S+)\s+.', self.stdout, 1, float)

    @performance_function('MBytes/sec', perf_key='Mul')
    def extract_scale_perf(self):
        return sn.extractsingle(r'Mul \s+(\S+)\s+..', self.stdout, 1, float)

    @performance_function('MBytes/sec', perf_key='Add')
    def extract_add_perf(self):
        return sn.extractsingle(r'Add \s+(\S+)\s+.?', self.stdout, 1, float)

    @performance_function('MBytes/sec', perf_key='Triad')
    def extract_triad_perf(self):
        return sn.extractsingle(r'Triad \s+(\S+)\s+.', self.stdout, 1, float)
    @performance_function('MBytes/sec', perf_key='Dot')
    def extract_dot_perf(self):
        return sn.extractsingle(r'Dot \s+(\S+)\s+.', self.stdout, 1, float)

@rfm.simple_test
class BablestreamGCC(Babelstream):
    valid_prog_environs = ['spack-gcc']
    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['babelstream%gcc+omp flags="-Ofast -march=native"']

@rfm.simple_test
class BablestreamAOCC(Babelstream):
    valid_prog_environs = ['spack-aocc']
    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['babelstream%aocc+omp flags="-Ofast -march=native"']

@rfm.simple_test
class BablestreamNVHPC(Babelstream):
    valid_prog_environs = ['spack-nvhpc']
    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['babelstream%nvhpc+omp flags="-Ofast -march=native"']

@rfm.simple_test
class BablestreamOneAPI(Babelstream):
    valid_prog_environs = ['spack-oneapi']
    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['babelstream%oneapi+omp flags="-Ofast -march=native"']
