mkdir $1/$2
./run.sh dumpdata questions > $1/$2/questions.json
./run.sh dumpdata labels > $1/$2/labels.json
tar -zcf $1/$2/media.tar.gz media/

