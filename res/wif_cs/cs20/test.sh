#! /bin/bash

for i in {0..199}
do
  old_fname="$(printf %03g $i).f.png"
  if [ -e $old_fname ]
  then
    echo -n "$old_fname >>"
    row=$(($i/10%10+1))
    col=$(($i%10+1))
    if [ $i -gt 99 ]; then
      col=$(($col+10))
    fi
    new_fname=$(printf %02d $row)"_"$(printf %02d $col)".png"
    echo "$new_fname"
    
    mv $old_fname $new_fname
  fi
done