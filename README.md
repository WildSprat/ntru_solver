# ntru_solver
Solving NTRU with lattice reduction
This repository contains the scripts accompanying the article

**Cyclotomic Ring, Almost-Parallel Hints, and Sieving for NTRU Attacks**


//# Contributers
//* anonymous

# Requirements

* [fpylll](https://github.com/fplll/fpylll)
* [g6k](https://github.com/fplll/g6k)
* [SageMath 9.3+](https://www.sagemath.org/) (required only if one wants to solve [NTRU Challenges](https://web.archive.org/web/20160310141551/https://www.securityinnovation.com/uploads/ntru-challenge-parameter-sets-and-public-keys-new.pdf))


# Description of files
Short description of the content:
* `attack_ntru.py` main file to run lattice reduction attack on NTRU
* `keygen.py` generates NTRU-HRSS and NTRU-HPS parameters
* `custom_pump.py` is a modified pump function from the  [g6k](https://github.com/fplll/g6k) library
* `pre_processing.py` preprocesses lattice bases of type 'slice', 'projected', 'challenge'
* `post_processing.py` post-processes the shortest vector found during the reduction
* `utils.py` contains helping functions
* `dual_basis.sage` computes the dual basis


# How to use

Run `attack_ntru.py` with the following parameters

* {HRSS, HPS, C} : NTRU type as per [NIST 3rd Round Specification document](https://ntru.org/f/ntru-20190330.pdf). Obligatory parameter
* `n` : defines NTRU ring x^n - 1. Integer. Obligatory parameter
* `-q`: NTRU modulus
* `--lattice_type` :  either of the following lattices {classic, classic_slice,phi, phi_projected, phi_projected_slice, challenge}
* `--nsamples` : Number of samples/rows of rot(h) used. Integer
* `--seed`: randomness seed to the NTRU key generation.
* `----pseudoinverse`: If True, use pseudoinverse of h as described [here](https://csrc.nist.gov/CSRC/media/Events/third-pqc-standardization-conference/documents/accepted-papers/nguyen-boosting-hybridboost-pqc2021.pdf)

* `-t` (or `--trials`): number of experiments to run per NTRU dimension (same NTRU type)
* `-w` (or `--workders`): number of parallel experiments to run
* `--threads`: number of threads used by 1 worker

BKZ-related parameters:

* `--bkz_alg`: either of following {fpylll, pump_n_jump}. Choose fpylll for enumeration, pump_n_jump for sieving as SVP oracles
* `--bkz_betas`: string of the form bkz_beta_start:bkz_beta_end:beta_step
* `--bkz_pre_beta`: blocksize for preprocessing (run BKZ with enumeration up to bkz_pre_beta (inclusive)). Integer
* `--bkz_tours`: number of bkz tours per blocksize. Integer


Sieving related parameters:

* `--sieve`: either of the following sieving algorithms {nv, bgj1, gauss, hk3, bdgl}
* `--sieve_jump`: determines by how much dimension we move between the sieving context. Integer.
* `--pump_down_sieve`: boolean that determines whether we sieving during the pump down
* `--dim4free`: string of the form a:b that determines the dimensions for free as a+b*blocksize.

* `--dump`: boolean that determines whether to dump the current basis after each blocksize is finished. Dumps bases to folder basis_dumps/
* `--filename`: name of the file to dump bases. The file will be named $filename+seed.txt
* `--readfrom`: filename to read the input basis from. It will be read from basis_dumps/$readfrom

* `--check_in_preprocessing`: boolean that determines whether to check for SKR during the preprocessing
* `--sage`: command to run sage on your machine. only necessary, when using a sliced lattice


# Experiments

To attack an NTRU-HRSS instance over x^111 - 1 using enumeration simply run
```
python ./attack_ntru.py HRSS 111 --verbose=True
```

It takes approximately half a minute on a laptop.
The script generates a random instance of NTRU-HRSS parameters according to the [NIST 3rd Round Specification document](https://ntru.org/f/ntru-20190330.pdf).

To generate an NTRU instance with a specific seed run

```
python ./attack_ntru.py HRSS 111 --seed=1
```

This run takes 34sec. on Apple M1 Pro and the shortest vector is found at blocksize 11.


To attack an NTRU-HPS instance over x^121 - 1 with q=512 run
```
python ./attack_ntru.py HPS 121 -q=512 --alg_bkz=pump_n_jump --verbose=True
```
It takes approximately 1h30 on a laptop to find a shortest vector.


TODO: describe the command for the plots
