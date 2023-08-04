import matplotlib.pyplot as plt
import librosa
import librosa.display
from matplotlib import cm

def plot_data(ax, data, sample_rate, hop_length, win_length, n_fft):

    """
    :param ax: Axes or array of Axes
    :param data: Matrix to display (e.g., spectrogram, mfcc)
    :param sample_rate: Sample rate used to determine time scale in x-axis.
    :param hop_length:
    :param win_length:
    :param n_fft: Number of samples per frame in STFT/spectrogram displays.
    """

    librosa.display.specshow(data, ax=ax,
                                   sr=sample_rate,
                                   hop_length = hop_length,
                                   win_length=win_length,
                                   y_axis='mel',
                                   x_axis='frames',
                                   n_fft = n_fft,
                                   cmap=cm.jet)

    ax.set(title='Log-frequency power spectrogram')
    ax.label_outer()

def input_subplot_save(ax, sound_input, trimmed_input, emphasized_input):
    """
    :param ax: Axes or array of Axes
    :param sound_input:
    :param trimmed_input:
    :param emphasized_input:
    """
    ax[0].plot(sound_input)
    ax[0].set_title('Original Audio Sound')
    ax[1].plot(trimmed_input)
    ax[1].set_title('Trimmed Audio Sound')
    ax[2].plot(emphasized_input)
    ax[2].set_title('Emphasized Audio Sound')

def som_plot(ax, data, title, colorbar: bool= False, aspect= 1.0, vmin=None, vmax=None, fraction = 0.15):
    """
    :param fraction: fraction of original axes to use for colorbar
    :param vmin, vmax: When using scalar data and no explicit norm, vmin and vmax define the data range that the
                       colormap covers.
    :param ax: Axes or array of Axes
    :param data: data to plot
    :param title: Title of the axis
    :param colorbar: If True, then colobar is plotted on the given axis
    :param aspect: The aspect ratio of the Axes.
    """
    im = ax.imshow(data, aspect=aspect, cmap='jet', origin="lower", vmin=vmin,vmax=vmax)
    ax.set_title(title)
    if colorbar:
        plt.colorbar(im, ax=ax, fraction=fraction)

def save_fig(fig, path, title='', dpi=100):
    """
    :param fig: Figure
    :param path: path to save figure
    :param title: Title of the figure
    :param dpi: The resolution in dots per inch
    """
    fig.suptitle(title)
    fig.savefig(path, bbox_inches='tight', dpi = dpi)