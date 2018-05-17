BENCHMARKS="bench"
CONTESTANTS=solvers/*.py
for bench in $BENCHMARKS
do
   echo "###" $bench "###"
   for file in $CONTESTANTS
   do 
      echo "###"
      echo $file 
      ./race-complete.py instances/$bench/ $file
      echo "###"
   done
done
