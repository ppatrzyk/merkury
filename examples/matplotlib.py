import matplotlib.pyplot as plt
from merkury.utils import output_matplotlib

intro = """
# Matplotlib usage

Example of how to include matplotlib plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

print(output_matplotlib(fig))
#HTML
