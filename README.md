# FigureManager

Just a simple window that holds all the plots created using matplotlib in a non blocking way while keeping interactivity.

https://github.com/user-attachments/assets/cda67a61-ea3c-4352-8c66-efb3ca68867e

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
