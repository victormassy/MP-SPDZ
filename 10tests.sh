cp input/input_MPCshare1_$1_v_$2.txt Player-Data/Input-P0-0
for i in {1..10} ; do
	./replicated-ring-party.x --player 0 ipae2e -ip Networking/coordination &> results.txt
	grep 'Time' results.txt | sed -e 's/Time = //' -e 's/seconds//' >> times.txt 
	grep 'Data sent' results.txt >> data.txt
done
