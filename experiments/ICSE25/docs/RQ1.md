# Replicating Results for RQ1

## Scanning packages using each Tool

In this section, we describe how to rerun each of the tool to generate the results for the analysis in 
rest of the sections RQ1-4. 

<details>
  <summary>Hercule</summary> 

### Hercule
We now describe how to reproduce the results for each of the data-set using `Hercule`

#### MalOSS Packages
```bash
python3 scripts/tools/hercule.py /data/maloss/ data-set/maloss
mv /opt/hercule/results /opt/hercule/results-maloss
cp /data/maloss/hercule_result.csv /experiments/hercule-maloss.csv
cp /data/maloss/rule_contribution.csv /experiments/hercule-maloss-rules.csv
```

#### BackStabber Packages
```bash
python3 scripts/tools/hercule.py /data/backstabber/ data-set/backstabber
mv /opt/hercule/results /opt/hercule/results-backstabber
cp /data/backstabber/hercule_result.csv /experiments/hercule-backstabber.csv
cp /data/backstabber/rule_contribution.csv /experiments/hercule-backstabber-rules.csv
```

#### MalRegistry Packages
```bash
python3 scripts/tools/hercule.py /data/malregistry/ data-set/malregistry
mv /opt/hercule/results /opt/hercule/results-malregistry
cp /data/malregistry/hercule_result.csv /experiments/hercule-malregistry.csv
cp /data/malregistry/rule_contribution.csv /experiments/hercule-malregistry-rules.csv
```

#### Popular Packages
```bash
python3 scripts/tools/hercule.py /data/top-100/ data-set/popular
mv /opt/hercule/results /opt/hercule/results-popular
cp /data/top-100/hercule_result.csv /experiments/hercule-popular.csv
cp /data/top-100/rule_contribution.csv /experiments/hercule-popular-rules.csv
```

#### Trusted Packages
```bash
python3 scripts/tools/hercule.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/results-trusted
cp /data/trusted/hercule_result.csv /experiments/hercule-trusted.csv
cp /data/trusted/rule_contribution.csv /experiments/hercule-trusted-rules.csv
```

</details>


<details>
  <summary>Bandit4Mal</summary> 

### Bandit4Mal
We now describe how to reproduce the results for each of the data-set using `bandit4mal`

#### MalOSS Packages
```bash
python3 scripts/tools/bandit.py /data/maloss/ data-set/maloss
mv /opt/hercule/results /opt/hercule/bandit-maloss
cp /data/maloss/bandit_result.csv /experiments/bandit-maloss.csv
```

#### BackStabber Packages
```bash
python3 scripts/tools/bandit.py /data/backstabber/ data-set/backstabber
mv /opt/hercule/results /opt/hercule/bandit-backstabber
cp /data/backstabber/bandit_result.csv /experiments/bandit-backstabber.csv
```

#### MalRegistry Packages
```bash
python3 scripts/tools/bandit.py /data/malregistry/ data-set/malregistry
mv /opt/hercule/results /opt/hercule/bandit-malregistry
cp /data/malregistry/bandit_result.csv /experiments/bandit-malregistry.csv
```

#### Popular Packages
```bash
python3 scripts/tools/bandit.py /data/top-100/ data-set/popular
mv /opt/hercule/results /opt/hercule/bandit-popular
cp /data/top-100/bandit_result.csv /experiments/bandit-popular.csv
```

#### Trusted Packages
```bash
python3 scripts/tools/bandit.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/bandit-trusted
cp /data/trusted/bandit_result.csv /experiments/bandit-trusted.csv
```

</details>


## SOTA Detailed Comparison (Table-II)
Once all the results are placed, following script will aggregate the results as shown in Table-II
Run the script using the command
```bash
python3 scripts/analysis/table-2.py
```
It will output the results for each tool-dataset combination as follows:
```bash
    ----- hercule ------
    DataSet TP FP TN FN
    popular 0 0 97 0

```

## SOTA High-Level Comparison (Table-III)
Upon completing the previous step, which will generate the aggregated data, following script will compute the results as shown in Table-III
Run the script using the command
```bash
python3 scripts/analysis/table-3.py
```
It will output the results for each tool-dataset combination as follows:
```bash
    Tool Precision Recall F1-Score FP-Rate Accuracy
    hercule 1.0 0.8801652892561983 0.9362637362637362 0.0 0.9144542772861357
```

