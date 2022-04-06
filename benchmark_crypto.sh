python3 crypto_benchmark.py

TIMEFORMAT='%3R'
TOTAL="0.0"

for i in {1..100}
do
   TIME=$( { time ./cryptominisat5-linux-amd64-gauss --verb 0 crypto_test/gauss_benchmark/$i.cnf > /dev/null; } 2>&1 | tr ',' '.')
   echo $TIME
   #(time ./cryptominisat5-linux-amd64-nogauss --verb 0 test_cnf/top$i.cnf) >> test_result/top$i.txt 2>&1
   TOTAL=$( echo "$TOTAL + $TIME"|bc )
done

echo "scale=4; $TOTAL / 100.000"|bc