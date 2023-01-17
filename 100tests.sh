./compile.py -R 32 ipae2e
for i in {1..10} ; do
	./10tests.sh $1 $i
done
