python3 singular_benchmark.py

TIMEFORMAT='%3R'
TOTAL="0.0"

for i in {1..100}
do
   TIME=$( { time Singular singular_test/slimgb_benchmark/$i.txt > /dev/null; } 2>&1 | tr ',' '.')
   echo $TIME

   TOTAL=$( echo "$TOTAL + $TIME"|bc )
   #TIME=$( { time Singular singular_test/std_benchmark/$i.txt > /dev/null; } 2>&1 )
done

echo "scale=4; $TOTAL / 100.000"|bc