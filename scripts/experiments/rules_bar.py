import pandas
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import margins

rule_groups = ["Exfiltration", "File", "Network", "Obfuscation", "Process"]
data_set_values = {
    'MalOSS': [220, 46, 274, 107, 73],
    'BackStabber':[112, 2, 179, 73, 63],
    'MalRegistry': [1355, 823, 902, 475, 182],
    'Popular': [5, 1, 6, 4, 1],
    'Trusted': [161, 31, 128, 198, 91]
}


x = np.arange(len(rule_groups))  # the label locations
print(x)
width = 0.1  # the width of the bars
multiplier = 0


fig, ax = plt.subplots()

for dataset_name, pkg_count in data_set_values.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, pkg_count, width, label=dataset_name)
    ax.bar_label(rects, padding=5)
    multiplier += 1


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Unique Package Count')
ax.set_xlabel('Behavior Class')
ax.set_xticks(x + 2*width, rule_groups)
ax.legend(loc='upper right', ncols=1)
ax.set_ylim(0, 1600)


# plt.show()
plt.savefig('rules.png')
