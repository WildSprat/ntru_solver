# ntru_solver
Solving NTRU with lattice reduction
This repository contains the scripts accompanying the article

**Cyclotomic Ring, Almost-Parallel Hints, and Sieving for NTRU Attacks**


# Contributers

* anonymous

# Requirements

* [fpylll](https://github.com/fplll/fpylll)
* [g6k](https://github.com/fplll/g6k)
* [SageMath 9.3+](https://www.sagemath.org/)


# Description of files
Short description of the content:
* attack_ntru.py TODO
* keygen.py TODO


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
It takes approximately TODO on a laptop


TODO: describe the command for the plots
