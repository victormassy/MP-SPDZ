./compile.py -R 32 ipae2e
for i in {1..10} ; do
	./replicated-ring-party.x --player 0 ipae2e -ip Networking/coordination &> results.txt
	#grep 'Time' results.txt >> times.txt 
	#grep 'Data sent' results.txt >> data.txt
done
