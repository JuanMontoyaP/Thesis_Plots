"""
This file contains the code for plotting all the data
"""
import os
import logging
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(
    format='[%(asctime)s] - %(levelname)s - %(filename)s - %(funcName)s:%(lineno)d - %(message)s',
    level=logging.DEBUG
)


class PlotGromacs:
    """
    Class for plotting data
    """

    def __init__(self, path):
        self.path = path
        self.images_path = path + "images/"

        try:
            os.makedirs(self.images_path)
            logging.info("Folder created successfully")
        except FileExistsError:
            logging.info("Folder already exists")

    def read_xvg_files(self, file_path):
        """
        Read data from xvg files.
        """
        data = []

        with open(file_path, 'r', encoding='utf8') as file:
            for line in file:

                if line.startswith('#') or line.startswith('@'):
                    continue

                values = [float(val) for val in line.strip().split()]
                data.append(values)

        data_array = np.array(data, dtype=float)
        return data_array

    def plot_data(self, x, y, titles):
        """
        Plot the specified data
        """
        fig, ax = plt.subplots()

        ax.plot(x, y, color='black', linewidth=0.7)

        # Add labels and title
        plt.xlabel(titles[0])
        plt.ylabel(titles[1])
        plt.title(titles[2])

        if len(titles) == 4:
            plt.legend(titles[-1])

        plt.xlim(left=x[0], right=x[-1])

        plt.minorticks_on()

        plt.tick_params(axis='both', which='both',
                        direction='in', right=True, top=True)

        return fig

    def plot_rms(self, data_file, protein_name):
        """
        Plot rms
        """
        logging.info("Plotting rms")
        data = self.read_xvg_files(self.path + data_file)

        _ = self.plot_data(
            data[:, 0],
            data[:, 1],
            [
                'Time $(ns)$',
                'RMSD $(nm)$',
                f"{protein_name}, Backbone"
            ]
        )

        plt.suptitle('RMSD', fontsize=20, y=1)

        plt.savefig(
            self.images_path + "RMSD.png",
            bbox_inches='tight',
            pad_inches=0.1,
            dpi=300
        )

    def plot_gyr(self, data_file, protein_name):
        """
        PLot radius of gyration
        """
        logging.info("Plotting rms")
        data = self.read_xvg_files(self.path + data_file)

        _ = self.plot_data(
            data[:, 0]/1000,
            data[:, 1],
            [
                'Time $(ns)$',
                '$R_{g} \\: (nm)$',
                protein_name
            ]
        )

        plt.ylim(bottom=1.3, top=6)

        plt.suptitle('Radius of gyration', fontsize=20, y=1)

        plt.savefig(
            self.images_path + "radius.png",
            bbox_inches='tight',
            pad_inches=0.1,
            dpi=300
        )
