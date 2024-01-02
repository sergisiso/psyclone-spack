import os
import glob
import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class HPCG(rfm.RegressionTest):
    descr = 'HPCG test using Spack version'
    valid_systems = ['+mpi_only']
    valid_prog_environs = ['builtin']
    executable = 'xhpcg'
    num_cpus_per_task = 1
    num_tasks = required
    num_tasks_per_node = required
    # executable_opts = ['--help']
    build_system = 'Spack'
    # hpcg.dat sets size of grid
    prerun_cmds.append('cp "$(dirname $(which xhpcg))/hpcg.dat" .')

    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['hpcg%gcc']

    @run_after('setup')
    def setup_variables(self):
        # One full node with one MPI process per core
        cores = int(self.current_partition.processor.num_cpus /
                    self.current_partition.processor.num_cpus_per_core)
        self.set_var_default('num_tasks', cores)
        self.set_var_default('num_tasks_per_node', cores)
        
    @run_after('run')
    def set_output_datafile(self):
        # If other outputfiles in stage directory before running, ensure use latest one
        possible_outfiles = glob.glob(self.stagedir + "/HPCG*.txt")
        if (len(possible_outfiles) >= 1):
            ordered_outfiles = sorted(possible_outfiles, key=lambda t: os.stat(t).st_mtime)
            self.output_data  = ordered_outfiles[-1]
        else:
            self.output_data = '' #no data

    @run_before('sanity')
    def set_sanity_patterns(self):
        # Check that it's a valid run
        self.sanity_patterns = sn.assert_found(r'VALID with a GFLOP/s rating of=', self.output_data)

    @run_before('performance')
    def set_perf_patterns(self):
        # This performance pattern parses the output of the program to extract
        # the desired figure of merit.
        self.perf_patterns = {
            'GFLOP/s Total with convergence': sn.extractsingle(
                r'VALID with a GFLOP/s rating of=(\S+)',
                self.output_data, 1, float),
            'GFLOP/s DDOT': sn.extractsingle(
                r'GFLOP/s Summary::Raw DDOT=(\S+)',
                self.output_data, 1, float),
            'GFLOP/s WAXPBY': sn.extractsingle(
                r'GFLOP/s Summary::Raw WAXPBY=(\S+)',
                self.output_data, 1, float),
            'GFLOP/s SpMV': sn.extractsingle(
                r'GFLOP/s Summary::Raw SpMV=(\S+)',
                self.output_data, 1, float),
            'GFLOP/s MV': sn.extractsingle(
                r'GFLOP/s Summary::Raw MG=(\S+)',
                self.output_data, 1, float),
            'GFLOP/s Total (wo convergence)': sn.extractsingle(
                r'GFLOP/s Summary::Raw Total=(\S+)',
                self.output_data, 1, float),
            'Distributed Processes': sn.extractsingle(
                r'Machine Summary::Distributed Processes=(\S+)',
                self.output_data, 1, float),
            'Threads per process': sn.extractsingle(
                r'Machine Summary::Threads per processes=(\S+)',
                self.output_data, 1, float),
            'Global nx': sn.extractsingle(
                r'Global Problem Dimensions::Global nx=(\S+)',
                self.output_data, 1, float),
            'Global ny': sn.extractsingle(
                r'Global Problem Dimensions::Global ny=(\S+)',
                self.output_data, 1, float),
            'Global nz': sn.extractsingle(
                r'Global Problem Dimensions::Global nz=(\S+)',
                self.output_data, 1, float),
            'Processors npx': sn.extractsingle(
                r'Processor Dimensions::npx=(\S+)',
                self.output_data, 1, float),
            'Processors npy': sn.extractsingle(
                r'Processor Dimensions::npy=(\S+)',
                self.output_data, 1, float),
            'Processors npz': sn.extractsingle(
                r'Processor Dimensions::npx=(\S+)',
                self.output_data, 1, float),
            'Local nx': sn.extractsingle(
                r'Local Domain Dimensions::nx=(\S+)',
                self.output_data, 1, float),
            'Local ny': sn.extractsingle(
                r'Local Domain Dimensions::ny=(\S+)',
                self.output_data, 1, float),
            'Local nz': sn.extractsingle(
                r'Local Domain Dimensions::nz=(\S+)',
                self.output_data, 1, float),
        }

@rfm.simple_test
class HPCG_Excalibur(HPCG):
    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['hpcg-excalibur@hpcg_original%gcc']
        
@rfm.simple_test
class HPCG_LFRic(HPCG):
    # This test also need the dinodump.dat
    prerun_cmds.append('cp "$(dirname $(which xhpcg))/dinodump.dat" .')

    @run_before('compile')
    def setup_build_system(self):
        self.build_system.specs = ['hpcg-excalibur@hpcg_lfric%gcc']
