import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


with plt.xkcd():
    fig, ax = plt.subplots()  # Create a figure and axes object

    # Plot the data
    ax.plot([0, 11.69, 42.56, 58.08, 82.47], [560, 488, 292, 190, 25], color='black')
    ax.plot([0, 11.69, 42.56], [480, 282, 282], color='orange')
    ax.plot([42.56, 58.08], [277, 105], color='orange')

    # Set the title
    ax.set_title('One-pressure HRSG')

    # Set the x and y axis labels
    ax.set_xlabel('Q [MW]')
    ax.set_ylabel('T [°C]')

    plt.axhline(y=0, color='k')

    # Set the tick locations and labels for the x-axis
    ax.set_xticks([0, 11.69, 42.56, 58.08, 82.47])
    #ax.set_xticklabels(['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5'])

    # Set the tick locations and labels for the y-axis
    ax.set_yticks([560, 488, 292, 190, 25])
    #ax.set_yticklabels(['Label1', 'Label2', 'Label3', 'Label4', 'Label5'])

    ax.annotate(
        'THINGS GOT A BIT\n CLUMSY AT THIS POINT',
        xy=(42.56, 292), arrowprops=dict(arrowstyle='->'), xytext=(35, 400))

    fig.text(
        0.5, 0.15,
        'Boilers are funnier with matplotlib',
        ha='center')

    plt.show()