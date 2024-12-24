import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

# ==========================================================
    

def scatter_hist(x, y, ax, ax_histx, ax_histy,nbins,labels):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y,s=150)
    ax.set_ylabel('Known Sample Labels', fontsize=18);
    ax.set_xlabel('Unsupervised Cluster Labels', fontsize=18);
    
    ax.set_yticks(range(int(np.amax(y))+1))
    ax.set_ylim([-0.5,np.amax(y)+.5])
    ax.set_xticks(range(int(np.amax(x))))
    ax.set_xlim([-0.5,np.amax(x)+.5])
    
    ax.grid()
    ax.tick_params(axis='both', labelsize=15)
    #plt.title(n_cluster, fontsize=12)
    #ax.set_xticks(fontsize=12)
    #ax.set_yticks(fontsize=12)
    
    #set the y tick labels from data
    ax.set_yticklabels(labels)    

    # now determine nice limits by hand:
    binwidth = 0.4
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(0, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=nbins,color = "lightsteelblue")
    ax_histy.hist(y, bins=nbins, orientation='horizontal',color = "salmon")
    
    ax_histx.set_ylabel('# samples', fontsize=18);
    ax_histx.tick_params(axis='both', labelsize=15)
    ax_histy.set_xlabel('# samples', fontsize=18);
    ax_histy.tick_params(axis='both', labelsize=15)    
    
 # ==========================================================


def pcolor_hist(array, ax, ax_histx, ax_histy,nbins,labels):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    #generate binary array of input
    binary_array = np.zeros(np.shape(array))
    binary_array[array != 0] = 1
    
    #project on either side and make binary
    x = np.sum(array,axis=1) #sum to get row vector
    y = np.sum(array,axis=0) #sum to get column
    
    #normalize along columns
    array = array / np.max(array, axis=0) 
    
    # the scatter plot:
    #ax.pcolor(binary_array,cmap='binary')
    ax.pcolor(array,cmap='binary')
    
    # Set the color limits to make the nonzero points gray
    #plt.clim(0, 1)
    
    ax.set_ylabel('Known Sample Labels', fontsize=18);
    ax.set_xlabel('Unsupervised Cluster Labels', fontsize=18);
    
    ax.set_xticks(np.arange(binary_array.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(binary_array.shape[0]) + 0.5, minor=False)
    ax.set_xticklabels(np.arange(binary_array.shape[1]))
    #ax.set_yticklabels(np.arange(binary_array.shape[0])

    # ax.set_yticks(range(len(y)))
    #ax.set_ylim([-0.5,len(y)+.5])
    # ax.set_xticks(range(len(x)))
    #ax.set_xlim([-0.5,len(x)+.5])
    ax.set_xlim([0,len(y)])
    
    ax.set_ylim([0,len(x)])
    
    ax.grid()
    ax.tick_params(axis='both', labelsize=15)
    #plt.title(n_cluster, fontsize=12)
    #ax.set_xticks(fontsize=12)
    #ax.set_yticks(fontsize=12)
    
    #set the y tick labels from data
    ax.set_yticklabels(labels)    
    ax.minorticks_on()  # Turn on minor ticks
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    
    # Set grid lines for minor ticks only
    ax.grid(which='minor', linestyle='-', linewidth=0.5)

    # Turn off grid lines for major ticks
    ax.grid(which='major', linestyle='None')

    # now determine nice limits by hand:
    binwidth = 0.4
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(0, lim + binwidth, binwidth)
    ax_histx.bar(np.arange(len(y))+.5,y, color = "lightsteelblue")
    ax_histy.barh(np.arange(len(x))+.5,x, color = "salmon")
    #ax_histx.hist(x, bins=nbins,color = "lightsteelblue")
    #ax_histy.hist(y, bins=nbins, orientation='horizontal',color = "salmon")
    
    ax_histx.set_ylabel('# samples', fontsize=18);
    ax_histx.tick_params(axis='both', labelsize=15)
    ax_histy.set_xlabel('# samples', fontsize=18);
    ax_histy.tick_params(axis='both', labelsize=15)    


    
    
    

    