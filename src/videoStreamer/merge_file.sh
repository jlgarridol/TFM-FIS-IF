#!/bin/bash

route=$1
file=$2
name=$3

mkdir tmp
cp $route/$file tmp
cd tmp

tar -xaf $file
r="./home/paciente/Descargas"
for i in $(ls $r)
do
    echo "file '"$r"/"$i"'" >> mylist.txt
done
ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.webm 2>/dev/null >> /dev/null

ffmpeg -i output.webm $name 2>/dev/null >> /dev/null

segundos=$(ffmpeg -i $name 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print 3600*A[1] + 60*A[2] + B[1] }')
echo $segundos
cp $name ../videos/processed/

cd ..
rm -rf tmp
