import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as cm
import numpy as np

#create a function containing all the plotting functionality we need 

#https://stackoverflow.com/questions/49709030/bar-plot-with-polar-axis
#https://www.python-graph-gallery.com/web-circular-lollipop-plot-with-matplotlib
#https://www.python-graph-gallery.com/circular-barplot-basic

def plot_single_classification(data,labels,fig,ax,centerlabel,text,lowerLimit):
    ###################
    #data is the vector of probabilities
    #labels is the names of categories we have probabilities for
    #fig,ax specify axes handles
    #centerlabel is what to put in the center of the plot (sample number, perhaps overall title)
    #text is scale for text size of the plot
    #lowerlimit is the threshold below which to call probabilities zero
    ###################
    
    # set figure size
    #fig=plt.figure(figsize=(10,10))

    # plot polar axis
    #ax = plt.subplot(111, polar=True)
    #ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], polar=True)

    # Remove lines for polar axis (x)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    

    # Remove spines
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color("none")

    # Let's compute heights: they are a conversion of each item value in those new coordinates
    # In our example, 0 in the dataset will be converted to the lowerLimit (10)
    # The maximum will be converted to the upperLimit (100)
    # slope = (max - lowerLimit) / max
    # heights = slope * df.Value + lowerLimit

    # Compute the width of each bar. In total we have 2*Pi = 360°
    width = 2*np.pi / len(data)

    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(data)+1))
    angles = [element * width for element in indexes]

    rotations = np.rad2deg(angles)
    #y0,y1 = ax.get_ylim()

    maxV = np.amax(data)
    maxI = np.where(data == maxV)
    maxI=maxI[0][0]

    # little space between the bar and the label
    labelPadding = .05
    #offset of inner ring in plot
    inner=0.45

    y0,y1 = ax.get_ylim()

    # Draw bars
    bars = ax.bar(
        x=angles, 
        height=data, 
        width=width, 
        bottom=lowerLimit+inner,
        linewidth=1.5, 
        edgecolor="black")

    ax.bar(
        x=angles[maxI], 
        height=data[maxI],
        width=width,
        bottom=lowerLimit+inner,
        linewidth=1.5, 
        edgecolor="black",
        color="firebrick")

    ax.bar(
    x=angles, 
    height=1+inner,
    width=width-0.03,
    bottom=lowerLimit,
    color="#f39c12", alpha=0.2)

    GREY97 = "#f3f3f3"
    ax.fill(angles, np.repeat(inner, len(angles)), GREY97)

    plt.axis('off')


    for x, bar, rotation, label in zip(angles, bars, rotations, labels):
     offset = (1+.03)#/(y1-y0) offset = (inner+bar.get_height()+.05)#/(y1-y0)
     lab = ax.text(0, 0, label, transform=None, 
             ha='center', va='center',fontsize=text)
     renderer = ax.figure.canvas.get_renderer()
     bbox = lab.get_window_extent(renderer=renderer)
     invb = ax.transData.inverted().transform([[0,0],[bbox.width,0] ])
     lab.set_position((x,offset+(invb[1][0]-invb[0][0])/2.*2.7 ) )
     lab.set_transform(ax.get_xaxis_transform())
     lab.set_rotation(rotation)

     offset2 = (.75*inner+bar.get_height())#/(y1-y0)
     if bar.get_height()>0.1:
        height = float('%.2g' % bar.get_height())    
            # Flip some labels upside down
    # Labels are rotated. Rotation must be specified in degrees 
        ang = np.deg2rad(rotation)
        rot = rotation

        # Flip some labels upside down
        alignment = ""
        if ang >= np.pi/2 and ang < 3*np.pi/2:
            alignment = "right"
            rot = rot + 180
        else: 
            alignment = "left"

        # Finally add labels for the height of the bars
        ax.text(
            x=ang, 
            y=inner + bar.get_height() + labelPadding, 
            s=height, 
            ha=alignment, 
            va='center', 
            rotation=rot,fontsize=text+2, 
            rotation_mode="anchor")

    ax.text(
        x=0.5, y=0.5, s=centerlabel,
        color='black', va="center", ha="center", ma="center",
        fontsize=text+4, fontweight="bold", linespacing=0.87, transform=ax.transAxes
    )#fontfamily='Times New Roman',
        # Put grid lines for radial axis (y) at 0, 1000, 2000, and 3000
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_yticks([])#0,.25, .5, .75, 1])


