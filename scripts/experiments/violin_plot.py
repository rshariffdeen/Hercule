import plotly.graph_objects as go
import plotly

array_y = {}
ranking = {}

datasets = ["MalOSS", "BackStabber", "MalRegistry", "Popular", "Trusted"]

fig = go.Figure()


for d in datasets:
    file_name = f"data/{d.lower()}"
    data = open(file_name, "r").readlines()
    sorted_data = sorted([float(t) for t in data])
    print(d, len(sorted_data))
    fig.add_trace(go.Violin(y=sorted_data,
                            name=d,
                            box_visible=True,
                            meanline_visible=True))

fig.update_layout(yaxis_zeroline=False, font=dict(
        family="Courier New, monospace",
        size=26
    ), legend=dict(
                orientation="h", xanchor="right", yanchor="top", y=1.2, x=1)
)
fig.show()
fig.show()
# html file
plotly.offline.plot(fig, filename='time.html')
