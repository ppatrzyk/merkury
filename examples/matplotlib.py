import matplotlib.pyplot as plt
import mpld3

intro = """
# Matplotlib usage

Example of how to include matplotlib plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

html = mpld3.fig_to_html(fig)
print(html)
#HTML
