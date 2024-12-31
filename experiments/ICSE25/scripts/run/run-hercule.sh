python3 scripts/tools/hercule.py /data/maloss/ data-set/maloss
mv /opt/hercule/results /opt/hercule/results-maloss
cp /data/maloss/hercule_result.csv /experiments/hercule-maloss.csv
cp /data/maloss/rule_contribution.csv /experiments/hercule-maloss-rules.csv

python3 scripts/tools/hercule.py /data/backstabber/ data-set/backstabber
mv /opt/hercule/results /opt/hercule/results-backstabber
cp /data/backstabber/hercule_result.csv /experiments/hercule-backstabber.csv
cp /data/backstabber/rule_contribution.csv /experiments/hercule-backstabber-rules.csv

python3 scripts/tools/hercule.py /data/malregistry/ data-set/malregistry
mv /opt/hercule/results /opt/hercule/results-malregistry
cp /data/malregistry/hercule_result.csv /experiments/hercule-malregistry.csv
cp /data/malregistry/rule_contribution.csv /experiments/hercule-malregistry-rules.csv

python3 scripts/tools/hercule.py /data/popular/ data-set/popular
mv /opt/hercule/results /opt/hercule/results-popular
cp /data/popular/hercule_result.csv /experiments/hercule-popular.csv
cp /data/popular/rule_contribution.csv /experiments/hercule-popular-rules.csv

python3 scripts/tools/hercule.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/results-trusted
cp /data/trusted/hercule_result.csv /experiments/hercule-trusted.csv
cp /data/trusted/rule_contribution.csv /experiments/hercule-trusted-rules.csv

