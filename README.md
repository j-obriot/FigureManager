# FigureManager

Just a simple window that holds all the plots created using matplotlib in a non blocking way while keeping interactivity.

![demo](/demo/demo.mp4)

## Usage

```py
import matplotlib.pyplot as plt
import figuremanager # must be imported after matplotlib
figuremanager.start_figure_manager()

plt.plot(...)
plt.show()

plt.plot(...) # this plot will go into a new tab
plt.show()
```
