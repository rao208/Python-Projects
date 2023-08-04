import numpy as np
class SelfOrganizingMap:

    def __init__(self, grid_pos, radius=1.5):

        """
        :param grid_pos: n_rows x n_cols grid
        :param radius: the radius of the neighbourhood function i.e.the number of neighbours,
        which determines how far neighbour nodes are examined in the 2D grid when updating vectors.
        """

        self.radius = radius  # radius
        self.grid_pos = grid_pos

    # Euclidean distance
    @staticmethod
    def e_distance(weights, x):

        """
        :param x: input vector’s instance at iteration t
        :param weights: weights
        :return: the Euclidean distance of the input vector and the weight vector
        """

        # 2. Compute Euclidean distance between the input vector x(t) and the weight vector w_ij

        return np.sqrt(np.sum((weights - x[None, None, :]) ** 2, axis=2))


    # Best Matching Unit search

    def winning_neuron(self, dist):

        """
        :param dist: the Euclidean distance of the input vector and the weight vector
        :return: the best matching unit (BMU) and the distance of a node from the BMU
        """

        # 3. Track the node that produces the smallest distance t.

        best = np.min(dist)
        best_cords = np.argwhere(dist == best)
        best_cords = best_cords.reshape(-1)
        best_cords = best_cords[::-1]
        assert dist[best_cords[1], best_cords[0]] == np.min(dist)

        # 4. Calculate the distance a node from the BMU.
        distBMU = np.sqrt(np.sum((self.grid_pos - best_cords[:, None, None]) ** 2, axis=0))

        return distBMU, best_cords


    def decay(self, dist_node_bmu): #, step, max_step

        """
        :param dist_node_bmu: the distance of a node from the BMU
        :return: influence is the topological neighbourhood i.e. when a neuron is fired its neighbours will be more
        # excited than far way neurons.
        """
        # now compute how much to influence the elements

        # time_constant = max_steps/self.radius
        # self.current_radius = self.radius*np.exp(-step/time_constant)
        # return np.exp(-dist_node_bmu ** 2 / (2 * self.current_radius ** 2)), time_constant

        return np.exp(-dist_node_bmu ** 2 / (2 * self.radius ** 2))#, time_constant