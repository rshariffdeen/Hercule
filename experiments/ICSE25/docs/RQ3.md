# Replicating Results for RQ3

This experiment requires running of one additional tool `lastpymile` which is implemented
as part of `hercule`. In order to generate the results of `lastpymile`, we have prepared a separate script.

#### Popular Packages
```bash
python3 scripts/tools/lastpymile.py /data/popular/ data-set/popular
mv /opt/hercule/results /opt/hercule/lastpymile-popular
cp /data/popular/lastpymile_result.csv /experiments/lastpymile-popular.csv

```

#### Trusted Packages
```bash
python3 scripts/tools/lastpymile.py /data/trusted/ data-set/trusted
mv /opt/hercule/results /opt/hercule/lastpymile-trusted
cp /data/trusted/lastpymile_result.csv /experiments/lastpymile-trusted.csv

```


## Impact of Integrity Analysis (Table-V)
Once completing the steps in [RQ1](RQ1.md) and above instructions for `lastpymile`, which will generate the experiment data, following script will compute the results as shown in Table-III
Run the script using the command
```bash
python3 scripts/analysis/table-5.py
```
It will output the results for each tool-dataset combination as follows:
```bash
    DataSet BanditMal LastPyMile Hercule
    popular 19900 3562 (82.10) 2241 (88.74)

```


