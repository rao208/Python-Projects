import os
import numpy as np
import matplotlib.pyplot as plt
from SOM import SelfOrganizingMap
from data import data_pickle
from create_image_folder import create_folder
import plotting_helper

np.set_printoptions(suppress=True)

if __name__ == "__main__":

    ed_path = os.path.join(os.getcwd(), 'Results', 'ed_images')
    frame_path = os.path.join(os.getcwd(), 'Results', 'frames_images')
    ed_frame_path = os.path.join(os.getcwd(), 'Results', 'ed_frames_images')

    create_folder(ed_path)
    create_folder(frame_path)
    create_folder(ed_frame_path)

    #######################################################################################################################

    path = os.path.join(os.getcwd(), 'data/meta_data.pickle')
    inp, data = data_pickle.unpickle_data(path)

    #######################################################################################################################

    num_dims = data.shape[1]
    n_neuron = 5*np.sqrt(data.shape[1])
    dim = int(np.ceil(np.sqrt(n_neuron)))
    learning_rate = 0.5
    max_steps = 100
    w = np.random.uniform(np.min(data), np.max(data), (dim, dim, num_dims))

    X, Y  = np.meshgrid(np.arange(w.shape[1]), np.arange(w.shape[0]))
    pos = np.array((X,Y))
    som = SelfOrganizingMap(grid_pos=pos)
    frames = []

    #######################################################################################################################

    # figManager = plt.get_current_fig_manager()
    # figManager.window.showMaximized()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams.update({'font.size': 14})

    #######################################################################################################################

    for step in range(max_steps):
        for sound_ex in range(len(data)): # range(4)
            for frame in range(data.shape[-1]):
                euclidean_distance = som.e_distance(weights = w, x = data[sound_ex][:, frame])
                distance_node, bmu = som.winning_neuron(dist = euclidean_distance)
                neighbourhood_area = som.decay(dist_node_bmu=distance_node)
                w += learning_rate * neighbourhood_area[:, :, None] * (data[sound_ex][:, frame] - w)

    cols = 4
    rows = int(np.ceil(data.shape[-1] / cols))

    #######################################################################################################################

    for sound_ex in range(len(data)):

        fig0 = plt.figure(num=1, figsize = (39, 22))
        fig1 = plt.figure(num=2, figsize=(39, 22))
        fig2 = plt.figure(layout='constrained', figsize=(39, 22))
        subfigs = fig2.subfigures(nrows=rows, ncols=cols, wspace=0.05, hspace=0.1)
        subfigs = subfigs.ravel()

        for frame in range(data.shape[-1]):

            sound = np.expand_dims(data[sound_ex][:, frame], axis=1)
            euclidean_distance_frame = som.e_distance(weights=w, x=data[sound_ex][:, frame])
            im_ratio = euclidean_distance_frame.shape[1] / euclidean_distance_frame.shape[0]
            fraction =0.047 * im_ratio

            ################################################################################################################

            axs = subfigs[frame].subplots(1, 2)
            axs = axs.ravel()
            subfigs[frame].set_facecolor('0.8')
            print(frame)
            title2 = 'Min: {:.3f}, Max: {:.3f}'.format(np.min(data[sound_ex][:, frame]),
                                                       np.max(data[sound_ex][:, frame]))

            plotting_helper.som_plot(ax=axs[0], data=euclidean_distance_frame, title=title2, colorbar=True,
                                     fraction=fraction)
            plotting_helper.som_plot(ax=axs[1], data=sound, title='', aspect=0.02, vmin=0, vmax=1)
            subfigs[frame].suptitle('Frame {}'.format(frame), fontsize='x-large')

            ###############################################################################################################

            ax1 = fig1.add_subplot(rows, cols, frame + 1)
            plotting_helper.som_plot(ax=ax1, data=sound, title= 'Frame {}'.format(frame), aspect=0.02, vmin=0, vmax=1)
            ax1.axis('off')

            ################################################################################################################

            ax0 = fig0.add_subplot(rows, cols, frame+1)
            title0 = 'Frame {}, Min: {:.3f}, Max: {:.3f}'.format(frame,
                                                                 np.min(data[sound_ex][:, frame]),
                                                                 np.max(data[sound_ex][:, frame]))
            plotting_helper.som_plot(ax=ax0, data=euclidean_distance_frame, title = title0, colorbar=True, fraction=fraction)


            ################################################################################################################



        title_fig2 = 'Audio sample: {}'.format(inp[sound_ex])
        title_fig1 = 'Each frame of the Melspectrogram: Audio={}' .format(inp[sound_ex])
        title_fig0 = 'Euclidean Distance of trained weights and each frame of the Melspectrogram: Audio={}' .format(inp[sound_ex])

        plotting_helper.save_fig(fig= fig2, path = ed_frame_path + '/' + str(sound_ex) + '_ed_subplots.png',
                                 title = title_fig2)
        plotting_helper.save_fig(fig=fig1, path=frame_path + '/' + str(sound_ex) + '_subplots_frames.png',
                                 title=title_fig1)
        plotting_helper.save_fig(fig= fig0, path = ed_path + '/' + str(sound_ex) + '_ed_subplots.png',
                                 title = title_fig0)

        fig0.clear()
        fig1.clear()
        fig2.clear()