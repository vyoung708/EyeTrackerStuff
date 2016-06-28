import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import DateFormatter

import numpy as np


def create_plot_video_in_intervall( signal, output_file, interval_start, interval_stop, window=30, fps = 15 ):
    """
    This function generates a video of a plot animation (signal plot over time)
    :param signal: a dictionary with the following keys:
        data: 2d array where the first column is the time and the other columns are the signal channels
        name: string that describes the signals, used as title of the plot (e.g. accelerometer with id 15)
        labels: a list of strings used for the legend. The first item should be "time", the others are the name of the signals.
            --> len(labels) has to be equal with number of columns in data
    :param output_file: Path and name of the output video file
    :param interval_start: starting time of the animation as a timestamp (posix)
    :param interval_stop: end time of the animation as a timestamp (posix)
    :param window: size of the sliding window (displayed segment) in seconds
    :param fps: fps of the output video
    :return: None
    """
    print( "--> create signal video ", output_file)
    FFMpegWriter = manimation.writers['ffmpeg']
    title = signal["name"]
    metadata = dict(title=title, artist='Peter Hevesi',
            comment='igroups')
    writer = FFMpegWriter(fps=fps, metadata=metadata, bitrate=-1, codec="libx264", extra_args=['-pix_fmt', 'yuv420p'])

    data = np.array(signal["data"])

    times = [datetime.fromtimestamp(x) for x in data[:, 0]]

    current_time = datetime.fromtimestamp(interval_start)
    interval_stop = datetime.fromtimestamp(interval_stop)

    fig = plt.figure(figsize=(12,4), dpi=300)

    for i in range(1, data.shape[1] ):
        plt.plot(times,  data[:, i])
    #plt.plot(times,  data[:, 2])
    #plt.plot(times,  data[:, 3])

    plt.title( title )
    plt.legend( signal["labels"][1:] )

    plt.gca().xaxis.set_major_locator( MaxNLocator(15) )
    plt.gca().xaxis.set_major_formatter( DateFormatter("%H-%M-%S") )
    fig.autofmt_xdate()
    plt.grid()
    plt.tight_layout()
    plt.show()


    ax = plt.gca()
    vl = ax.axvline(color='k')  # the vert line


    with writer.saving(fig, output_file, 100):
        while current_time < interval_stop:
            plt.xlim( current_time - timedelta(seconds=window/2), current_time + timedelta(seconds=(window/2)))
            print( current_time, interval_stop - current_time)

            current_time = current_time + timedelta(seconds=1/fps)
            vl.remove()
            vl = ax.axvline(color='k', x=current_time)
            writer.grab_frame()

    print( "<-- ready.")
    plt.close()



if __name__ == '__main__':
	create_plot_video_in_intervall(...)