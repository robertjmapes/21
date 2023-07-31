for file in ./images/cards/*
do
  convert $file -resize 150x170 $file
done


