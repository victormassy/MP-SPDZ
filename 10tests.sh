cp input/input_MPCshare1_$1_v_$2.txt Player-Data/Input-P0-0
#only if you are testing on 1 VM 
#cp input/input_MPCshare2_$1_v_$2.txt Player-Data/Input-P1-0
#cp input/input_MPCshare3_$1_v_$2.txt Player-Data/Input-P2-0
for i in {0..9} ; do
	#if you are testing on 3 different VM (you need to update coordination file)
	./replicated-ring-party.x --player 0 ipae2e_original -ip Networking/coordination2 &> results.txt
	#if you are testing on 1 VM
	#Scripts/ring.sh ipae2e_original &> results.txt
	grep 'Time' results.txt | sed -e 's/Time = //' -e 's/seconds//' >> times.txt 
	grep 'Data sent' results.txt >> data.txt
done
