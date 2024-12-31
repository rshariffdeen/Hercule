python3 scripts/tools/bandit.py /data/maloss/ data-set/maloss
mv /opt/hercule/results /opt/hercule/bandit-maloss
cp /data/maloss/bandit_result.csv /experiments/bandit-maloss.csv

python3 scripts/tools/bandit.py /data/backstabber/ data-set/backstabber
mv /opt/hercule/results /opt/hercule/bandit-backstabber
cp /data/backstabber/bandit_result.csv /experiments/bandit-backstabber.csv

python3 scripts/tools/bandit.py /data/malregistry/ data-set/malregistry
mv /opt/hercule/results /opt/hercule/bandit-malregistry
cp /data/malregistry/bandit_result.csv /experiments/bandit-malregistry.csv

python3 scripts/tools/bandit.py /data/popular/ data-set/popular
mv /opt/hercule/results /opt/hercule/bandit-popular
cp /data/popular/bandit_result.csv /experiments/bandit-popular.csv

python3 scripts/tools/bandit.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/bandit-trusted
cp /data/trusted/bandit_result.csv /experiments/bandit-trusted.csv
