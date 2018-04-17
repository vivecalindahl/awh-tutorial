#! /usr/bin/env python2.7

# ======================================================
#
# IMPORTS
# ======================================================


# Execute global startup script
import os

startup = os.environ.get("PYTHONSTARTUP")
if startup and os.path.isfile(startup):
    execfile(startup)

import argparse
import inspect

# My own modules
import read_write as rw
import function_utils as fu

# ======================================================
#
# FUNCTIONS
# ======================================================

# Plot 2d function data
#---------------------------------------------------------
# Description:
#
#

def plot_2d(fnamelist, zcol=2, npoints=200, out="out.eps", sub=False,
            scatfname=None, scatcolor=None, scatcolorlabel=None,
            contours=False, contoursbar=False, contourslabels=False,
            noimage=False,
            zmin=None, zmax=None, xmin=None, xmax=None, ymin=None, ymax=None,
            title=None, xlabel='x', ylabel='y', zlabel='z'):

    # Want a list of filenames
    if type(fnamelist) != list:
        fnamelist = list(fnamelist)

    # Create a figure with a good number of subplots
    nfiles = len(fnamelist)

    ncols = 1
    while (True):
        nrows =  int(np.ceil(float(nfiles)/ncols))
        if nrows > 2*ncols:
            ncols += 1;
        else:
            break;

    fig, axisarray = plt.subplots(nrows, ncols, sharex=True, sharey=True)

    # Don't know how to do this properly :(
    if nfiles == 1:
        axisarray=np.array([axisarray])

    axisarray=axisarray.flatten()

    for (ax, fname) in zip(axisarray, fnamelist):
        fu.exit_if_not_exists(fname)

        # Activate next axis
        plt.axes(ax)

        # Read data
        data, comments = rw.read_xvg(fname)

        x, y = data[:,0], data[:,1]
        z = data[:,zcol]

        if sub:
            z=z-z.min()

            if not zmin:
                zmin = np.floor(z.min())
            if not zmax:
                zmax = np.ceil(z.max())

        # Set up x, y grid variables
        nx = ny = npoints
        if not xmin:
            xmin = x.min()
        if not xmax:
            xmax = x.max()
        if not ymin:
            ymin = y.min()
        if not ymax:
            ymax = y.max()

        xi, yi = np.linspace(xmin, xmax, nx), np.linspace(ymin, ymax, ny)
        Xi, Yi = np.meshgrid(xi, yi)

        # Rescale values so that x and y have similar ranges for numerical reasons
        xi, x, yi, y = xi/xmax, x/xmax, yi/ymax, y/ymax

        # Interpolate z on grid
        Z = plt.mlab.griddata(x, y, z, xi, yi, interp='linear')


        # Do contours
        # ----------------------------------------------------------------------------------------------
        if contours:
            contours_cmap = plt.cm.jet # seismic #PiYG

            if not contoursbar and not contourslabels:
                contours=plt.contour(Xi,Yi,Z, colors='black', extent=[xmin, xmax, ymin, ymax], aspect="auto")
            else:
                contours=plt.contour(Xi,Yi,Z, cmap=contours_cmap, extent=[xmin, xmax, ymin, ymax], aspect="auto")
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)        
            if contoursbar:
                cbarcountours = plt.colorbar(contours, shrink=0.8, orientation='horizontal') # Inherits colormap from contours
                #cbarcountours = plt.colorbar(contours, shrink=1, orientation='vertical') # Inherits colormap from contours
            if contourslabels:
                plt.clabel(contours, inline=1, fontsize=10)

        # Do scatter
        # ----------------------------------------------------------------------------------------------
        # Note: do this before the 2D image so that the axis are taken from the latter.
        if scatfname:
            fu.exit_if_not_exists(scatfname)

            data,_ = rw.read_xvg(scatfname)
            xscat, yscat = data[:,0], data[:,1]

            # Delete scatter data that is not in the axis range 
            xscat_inrange, yscat_inrange = xscat <= xmax, yscat <= ymax;
            xyscat_inrange = np.logical_and(xscat_inrange, yscat_inrange)
            xscat, yscat = xscat[xyscat_inrange], yscat[xyscat_inrange]

            if scatcolor:
                scat_cmap = plt.cm.seismic # PiYG

                if (data.shape[1] < 3):
                    sys.exit("Need 3rd column for " + scatfname)
                zscat = data[:, 2][xyscat_inrange]
                plt.scatter(xscat, yscat, marker='x', c=zscat, cmap=scat_cmap)
                plt.xlim(xmin, xmax)
                plt.ylim(ymin, ymax)
                cbarscat = plt.colorbar() # Inherits colorbar from scat axes
                if scatcolorlabel:
                    cbarscat.ax.set_ylabel(scatcolorlabel)
            else:
                plt.scatter(xscat, yscat, marker='x', color='black')

        # Do image
        # ----------------------------------------------------------------------------------------------
        if not noimage:
            im_cmap = plt.cm.jet
            im=plt.imshow(Z, origin='lower', extent=[xmin, xmax, ymin, ymax], aspect="auto",
                          cmap=im_cmap)

            # z axis (colorbar)
            max_zticks = 5
            zloc = plt.MaxNLocator(max_zticks)
            cbar = plt.colorbar(ticks=zloc)
            cbar.ax.set_ylabel(zlabel)
            plt.clim(zmin,zmax)

            # Reduce the automatic no of ticks for x, y if there
            # are multiple plots
            if nfiles > 1:
                max_xticks = 5
                xloc = plt.MaxNLocator(max_xticks)
                ax.xaxis.set_major_locator(xloc)
                max_yticks = 5
                yloc = plt.MaxNLocator(max_yticks)
                ax.yaxis.set_major_locator(yloc)

            #im.set_data(Z) # Needed?

        # Final  tuning
        # ----------------------------------------------------------------------------------------------
        # x, y axes
        if nfiles == 1:
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

        if title:
            ax.set_title(title)


    # Done. Write to output.
    plt.savefig(out)
    print "Saving to file " + out

#--------------------------------------------
# Main function
#--------------------------------------------

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="plot 2d data")

    # Positional args
    parser.add_argument('filename', type=str, nargs='+', help='data file to plot')

    # Optional args
    parser.add_argument("--out", "-o", type=str, help="output file")
    parser.add_argument("--zcol", type=int, help="column to plot")
    parser.add_argument("--npoints", "-n", type=int, help="number of grid points (per dim)")
    parser.add_argument("--sub", action='store_true', help="subtract minimum from z")

    parser.add_argument("--scatfname", type=str, help='data file to scatter plot')
    parser.add_argument("--scatcolor", action='store_true', help="color scatter plot markers by z")
    parser.add_argument("--scatcolorlabel", type=str, help='label for scatter colorbar')

    parser.add_argument("--contours", action='store_true', help="plot contours")
    parser.add_argument("--contoursbar", action='store_true', help="plot contour colorbar")
    parser.add_argument("--contourslabels", action='store_true', help="plot contour labels")

    parser.add_argument("--noimage", action='store_true', help="do not plot image")
    parser.add_argument("--xmin", type=float, help="max x")
    parser.add_argument("--xmax", type=float, help="min x")
    parser.add_argument("--ymin", type=float, help="max x")
    parser.add_argument("--ymax", type=float, help="min x")
    parser.add_argument("--zmin", type=float, help="max z")
    parser.add_argument("--zmax", type=float, help="min z")
    parser.add_argument("--title", type=str, help='title in plot')
    parser.add_argument("--xlabel", type=str, help='x-axis label')
    parser.add_argument("--ylabel", type=str, help='y-axis label')
    parser.add_argument("--zlabel", type=str, help='z-axis label')

    parsed_args = parser.parse_args()

    defaults=fu.get_default_args(plot_2d)

    argdict = {}

    for arg in vars(parsed_args):
        attr = getattr(parsed_args, arg)
        if not attr and defaults.has_key(arg):
            argdict[arg] = defaults[arg]
        else:
            argdict[arg] = attr

    filename = parsed_args.filename

    plot_2d(filename, zcol=argdict['zcol'], npoints=argdict['npoints'], out=argdict['out'], sub=argdict['sub'],
            contours=argdict['contours'], contoursbar=argdict['contoursbar'], contourslabels=argdict['contourslabels'],
            noimage=argdict['noimage'],                     
            scatfname=argdict['scatfname'], scatcolor=argdict['scatcolor'], scatcolorlabel=argdict['scatcolorlabel'],
            zmin=argdict['zmin'], zmax=argdict['zmax'], xmin=argdict['xmin'], xmax=argdict['xmax'],
            ymin=argdict['ymin'], ymax=argdict['ymax'],
            title=argdict['title'], xlabel=argdict['xlabel'], ylabel=argdict['ylabel'], zlabel=argdict['zlabel'])
