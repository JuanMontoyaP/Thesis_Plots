"""
This script graphs the results of MD simulations
"""
#!/usr/bin/env python3 -u
import subprocess
import logging
import click

from plot_gromacs import PlotGromacs

logging.basicConfig(
    format='[%(asctime)s] - %(levelname)s - %(filename)s - %(funcName)s:%(lineno)d - %(message)s',
    level=logging.DEBUG
)


class PlotMolecularDynamics:
    """
    Plot the results of the molecular dynamics simulation
    """

    def __init__(self, path: str, protein: str):
        self.path = path
        self.protein = protein

    def generate_gromacs_data(self):
        """
        This function generates all the data needed to plot the results.
        """
        logging.info("Generating all the data needed to plot the results")
        subprocess.run(
            ["zsh", "rms_gyr.sh", self.path],
            check=True,
        )

    def Run(self, gromacs_flag: bool):
        """
        The function that orchestrates the procedure.
        """
        if gromacs_flag:
            self.generate_gromacs_data()

        plot = PlotGromacs(self.path)
        plot.plot_rms("rmsd.xvg", self.protein)
        plot.plot_gyr("gyrate.xvg", self.protein)


@click.command()
@click.option(
    '--path',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True
    ),
    help="Path where the data files should be.",
    required=True
)
@click.option(
    '--protein',
    type=str,
    required=True,
    help="Name of the protein to be plotted"
)
@click.option(
    '--gromacs',
    is_flag=True,
    help='False if you dont need to generate gromacs data'
)
def cli(path: str, protein: str, gromacs: bool = False):
    """
    Docstring
    """
    if path[-1] != "/":
        path = path + "/"

    md = PlotMolecularDynamics(path, protein)
    md.Run(gromacs)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
