python3 scripts/tools/lastpymile.py /data/popular/ data-set/popular
mv /opt/hercule/results /opt/hercule/lastpymile-popular
cp /data/popular/lastpymile_result.csv /experiments/lastpymile-popular.csv

python3 scripts/tools/lastpymile.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/lastpymile-trusted
cp /data/trusted/lastpymile_result.csv /experiments/lastpymile-trusted.csv

