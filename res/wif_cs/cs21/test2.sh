#! /bin/bash

shift=3

for i in {199..189}
do
  old_fname="$(printf %03g $i).f.png"
  if [ -e $old_fname ]
  then
    echo -n "$old_fname >>"
    
    new_fname="$(printf %03g $((i+$shift))).f.png"
    
    echo "$new_fname"
    
    mv $old_fname $new_fname
  fi
done