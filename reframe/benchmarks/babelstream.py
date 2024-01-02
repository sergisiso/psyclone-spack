import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Bablestream(rfm.RegressionTest):
    descr = 'Babelstream test using Spack OpenMP version'
    valid_systems = ['+omp_only']
    valid_prog_environs = ['builtin']
    executable = 'omp-stream'
    # executable_opts = ['--help']
    build_system = 'Spack'

    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['babelstream%gcc+omp']

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

    @run_after('performance')
    def upload_results(self):
        import pdb; pdb.set_trace()
        
