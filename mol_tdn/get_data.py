"""Get data from hardcoded csv files, and define constants."""
import os
import pandas as pd


def get_molecules_df():
    thisdir = os.path.dirname(os.path.realpath(__file__))
    return pd.read_csv(os.path.join(thisdir, "data", "molecules.csv"))


def get_periodic_table_df():
    thisdir = os.path.dirname(os.path.realpath(__file__))
    return pd.read_csv(os.path.join(thisdir, "data", "periodic_table.csv"))


# Tables
MOLECULE_DF = get_molecules_df()
PERIODIC_TABLE_DF = get_periodic_table_df()

# Constants
R = 8.314e-5
R_UNIT = "m^3*bar/K/mol"
