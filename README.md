# Private attribution reporting

This repo contains a prototype for privacy preserving attribution reporting in a secure enclave.

For more information check the paper: TODO

# Quickstart 

For MP-SPDZ installation please check the [main project](https://github.com/data61/MP-SPDZ). This project is directly forked from the MP-SPDZ project and installation is the same.

Our scripts are Programs/Source/ipae2e_original.mpc and Programs/Source/ipae2e_modified.mpc. These file are directly modified from [IPA research prototype](https://github.com/private-attribution/research-prototype)

# Run multiple tests
The script is designed to run on 3 different VM (for execution on 1VM check 10tests.sh file)
You must run the following command on 3 different VM. 

Some scripts can be used to run multiple tests. For these scipts to work, you need to follow these steps: 
 - Clone input repo 
 ```
 git clone https://github.com/victormassy/input.git
 ```
 
 - Unzip input the correct file. Example is given for an input size of 2**12:
 
```
cd input
unzip 12_trig3_users_100.zip
```
 - Update Networking/coordination file with your confifuration. Check MP-SPDZ [documentation](https://mp-spdz.readthedocs.io/en/latest/networking.html) to get support. 
 - Modify 10tests.sh according to your configuration. 
 - Setup SSL for the parties
```
Scripts/setup-ssl.sh 3
```
These creates keys stored in Player Data for execution on 3 VM you need to split the keys accordingly. (Party 0 has access to private key 0 and public key 0, 1 and 2) 
 - Run tests:
``` 
cd ..
chmod +x 100tests.sh 
chmod +x 10tests.sh
./100tests.sh 12 
```
Parameter of 100tests.sh is input size in power of two. 

If you want to test another input size, you need to update the value in ipae2e_original.mpc
You can test the modified version by replacing ipae2e_original.mpc with ipae2e_modified.mpc in 100tests.sh and 10tests.sh
Execution times are stored in file times.txt in seconds (s). 
