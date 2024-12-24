import pandas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import margins

rule_groups = ["File", "Network", "Obfuscation", "Process", "Exfiltration"]
data_set_values = {
    'True Positives': [ 1306, 1264, 438, 1263, 723],
    'False Positives':[69, 58, 10, 50, 20],
}


x = np.arange(len(rule_groups))  # the label locations
print(x)
width = 0.3  # the width of the bars
multiplier = 0


fig, ax = plt.subplots()

for dataset_name, pkg_count in data_set_values.items():
    offset = width * multiplier
    rects = ax.barh(x + offset, pkg_count, width, label=dataset_name)
    ax.bar_label(rects, padding=3)
    multiplier += 1


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Unique Package Count')
ax.set_ylabel('Behavior Class')
ax.set_yticks(x + 0.5*width, rule_groups)
ax.legend(loc='upper right', ncols=1)
ax.set_xlim(0, 1500)


# plt.show()
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig('rules.png', bbox_inches='tight')
