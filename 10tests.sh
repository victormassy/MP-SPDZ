#This code is meant to be executed on 3 VM you can uncomment one of the next lines
#First helper: 
#cp input/input_MPCshare1_$1_v_$2.txt Player-Data/Input-P0-0
#Second helper:
#cp input/input_MPCshare2_$1_v_$2.txt Player-Data/Input-P1-0
#Third helper: 
#cp input/input_MPCshare3_$1_v_$2.txt Player-Data/Input-P2-0

#If you want to test this script on 1VM you can uncomment the 3 lines.

for i in {0..9} ; do
	#if you are testing on 3 different VM 
	#First helper: 
	#./replicated-ring-party.x --player 0 ipae2e_original -ip Networking/coordination &> results.txt
	#Second helper:
	#./replicated-ring-party.x --player 1 ipae2e_original -ip Networking/coordination &> results.txt
	#Third helper: 
	#./replicated-ring-party.x --player 2 ipae2e_original -ip Networking/coordination &> results.txt
	
	#if you are testing on 1 VM
	#Scripts/ring.sh ipae2e_original &> results.txt
	
	grep 'Time' results.txt | sed -e 's/Time = //' -e 's/seconds//' >> times.txt 
	grep 'Data sent' results.txt >> data.txt
done
