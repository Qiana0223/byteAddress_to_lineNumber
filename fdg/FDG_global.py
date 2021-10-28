from copy import copy
import numpy as np
global control_level
control_level=2

global num_seq_limit
num_seq_limit=5

global print_ftn_coverage
print_ftn_coverage=1

# control the number of symbolic transactions issued by LaserEVM
global transaction_count
transaction_count=50

# provide them to FDG_pruner for FDG building
global solidity_path
global contract

# max depth of sequence in FDG is set to 5
global depth_all_ftns_reached
depth_all_ftns_reached=5

# save the coverage (from coverage_plugin)
global coverage
coverage=0

global target_bytecode
target_bytecode=''

# get instruction indices for each function (from soliditycontract)
global ftns_instr_indices
ftns_instr_indices={}

# save the lists that record which instruction is covered (from coverage_plugin)
global ftns_instr_cov
ftns_instr_cov=[]

global mapping
mapping=[]

global solc_indices

global method_identifiers
method_identifiers={}


