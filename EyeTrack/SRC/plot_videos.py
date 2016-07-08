import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as pll
import matplotlib.animation as manimation
from datetime import datetime, timedelta
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import DateFormatter

import numpy as np


def create_plot_video_in_intervall( signal, output_file, interval_start, interval_stop, window=30, fps = 10 ):
    print( "--> create signal video ", output_file)
    FFMpegWriter = manimation.writers['ffmpeg']
    title = "Origami Eye Movement p01"
    metadata = dict(title=title, artist='Victoria the magnificent',
            comment='igroups')
    writer = FFMpegWriter(fps=fps, metadata=metadata, bitrate=-1, codec="libx264", extra_args=['-pix_fmt', 'yuv420p'])


    fig = plt.figure(figsize=(6,4), dpi=300)
    xmin = np.min(signal[:, 0])
    xmax = np.max(signal[:, 0])
    ymin = np.min(signal[:, 1])
    ymax = np.max(signal[:, 1])
    with writer.saving(fig, output_file, 100):
        step = 3
        for i in range(0, len(signal)-step):
            plt.plot( signal[i:i+step,0 ], signal[i:i+step, 1], '.r-')
            num = i
            for j in range(i, i+step):
                plt.annotate(num, xy=(signal[j,0], signal[j, 1]), xytext = (signal[j,0 ] + 1, signal[j, 1] + 1))
                num += 1
            plt.gca().set_xlim([xmin, xmax])
            plt.gca().set_ylim([ymin, ymax])
            writer.grab_frame()
            plt.clf()
    print( "<-- ready.")
    plt.close()



if __name__ == '__main__':
    pass