# matplotlib examples

## Scatter plots
### Scatter plot with points on a colour scale and a colour bar
```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.random.rand(100)
scatter = ax.scatter(x, y, c=colors, cmap='viridis')
colorbar = fig.colorbar(scatter, ax=ax)
colorbar.set_label("intensity")
plt.show()
```
![](./matplotlib_examples/scatter_plot_with_points_on_a_colour_scale_and_a_colour_bar.png)