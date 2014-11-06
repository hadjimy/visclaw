"""
Interactive animations in IPython notebooks using matplotlib and JSAnimation.
"""


def ianimate(frame_list,plotdata=None,ivar=0,varname=None,**kargs):
    """
        frame_list may be:

            - a list of Solution objects
            - a controller possessing a list of Solution objects
    """
    import matplotlib.pyplot as plt
    from matplotlib import animation
    from clawpack.visclaw.JSAnimation import IPython_display
    from clawpack.pyclaw import Controller
    import numpy as np

    if isinstance(frame_list,Controller):
        frame_list = frame_list.frames

    frame = frame_list[0]
    ndim = len(frame.q.shape)-1

    if ndim == 1:
        fig = plt.figure(figsize=(10,6))
        ax = plt.axes()
        im, = ax.plot([], [],lw=2)
        
        xc = frame.state.grid.p_centers[0]
        ax.set_xlim(xc[0],xc[-1])
        ymax = max([np.max(f.q[ivar,:]) for f in frame_list])
        ymin = min([np.min(f.q[ivar,:]) for f in frame_list])
        ydiff = ymax-ymin
        ax.set_ylim(ymin-ydiff/10.,ymax+ydiff/10.)

        ax.set_xlabel('x')
        if varname is not None:
            ax.set_ylabel(varname)

    ivar = 0

    frame = frame_list[0]
    ndim = len(frame.q.shape)-1
    if ndim == 1:
        fig = plt.figure(figsize=(8,4))
        ax = plt.axes()
        xc = frame.state.grid.p_centers
        im, = ax.plot([], [])
    elif ndim == 2:
        fig = plt.figure(figsize=(4,4))
        xc, yc = frame.state.grid.p_centers
        im = plt.imshow(frame.q[ivar,:,:].T,
                extent = [xc.min(), xc.max(), yc.min(), yc.max()], 
                interpolation='nearest',origin='lower')


    def fplot(frame_number):
        frame = frame_list[frame_number]
        if varname is not None:
            fig.suptitle(varname+' at time t = '+str(frame.t))
        else:
            fig.suptitle('Time t = '+str(frame.t))
        if ndim == 1:
            im.set_data(xc, frame.q[ivar,:])
        elif ndim == 2:
            im.set_data(frame.q[ivar,:,:].T)
        else:
            raise Exception('3D animation not yet implemented')
        return im,

    return animation.FuncAnimation(fig, fplot, frames=len(frame_list))