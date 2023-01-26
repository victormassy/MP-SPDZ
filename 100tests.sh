#./compile.py -R 32 ipae2e
rm times.txt
rm data.txt
for i in {0..9} ; do
	./10tests.sh $1 $i
done
