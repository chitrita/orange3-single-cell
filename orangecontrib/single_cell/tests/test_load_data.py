import os
import unittest

import numpy as np
import numpy.testing as npt
import pandas as pd

from orangecontrib.single_cell.widgets.load_data import (
    MtxLoader, CountLoader, Loader, PickleLoader, get_data_loader
)


class TestLoadData(unittest.TestCase):
    def test_get_data_loader(self):
        self.assertIsInstance(get_data_loader("matrix.mtx"), MtxLoader)
        self.assertIsInstance(get_data_loader("lib.cell.count"), CountLoader)
        loader = get_data_loader("DATA_MATRIX_LOG_TPM.txt")
        self.assertIsInstance(loader, Loader)

    def test_get_data_loader_pickle(self):
        self.assertIsInstance(get_data_loader("data.pkl"), PickleLoader)
        self.assertIsInstance(get_data_loader("data.pickle"), PickleLoader)

    def test_get_data_loader_compressed_file(self):
        loader = get_data_loader("lib.cell.count.gz")
        self.assertIsInstance(loader, CountLoader)

    def test_file_summary_mtx(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/10x/hg19/matrix.mtx")
        loader = MtxLoader(file_name)
        self.assertEqual(loader.file_size, 112)
        self.assertEqual(loader.n_rows, 4)
        self.assertEqual(loader.n_cols, 6)
        self.assertEqual(loader.sparsity, 0.625)

    def test_file_summary_broad(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/DATA_MATRIX_LOG_TPM.txt")
        loader = Loader(file_name)
        self.assertEqual(loader.file_size, 1084)
        self.assertEqual(loader.n_rows, 10)
        self.assertEqual(loader.n_cols, 15)
        self.assertEqual(round(loader.sparsity, 2), 0.86)

    def test_file_summary_hhmi(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/lib.cell.count")
        loader = CountLoader(file_name)
        self.assertEqual(loader.file_size, 428)
        self.assertEqual(loader.n_rows, 10)
        self.assertEqual(loader.n_cols, 11)
        self.assertEqual(round(loader.sparsity, 2), 0.99)

    def test_file_summary_pickle(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/data.pkl")
        loader = PickleLoader(file_name)
        self.assertEqual(loader.file_size, 5021)
        self.assertEqual(loader.n_rows, None)
        self.assertEqual(loader.n_cols, None)
        self.assertEqual(loader.sparsity, None)

    def test_file_summary_gz(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/data.txt.gz")
        loader = Loader(file_name)
        self.assertEqual(loader.file_size, 361)
        self.assertEqual(loader.n_rows, 10)
        self.assertEqual(loader.n_cols, 15)
        self.assertEqual(round(loader.sparsity, 2), 0.86)

    def test_load_data_mtx(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/10x/mm10/matrix.mtx")
        loader = MtxLoader(file_name)
        df = pd.read_csv(file_name, sep=" ", header=None, skiprows=[0, 1])
        attrs, X, meta_df, meta_df_index = loader._load_data()
        array = np.zeros((df.iloc[0, 0], df.iloc[0, 1]))
        for i, series in df.iterrows():
            if i == 0:
                continue
            array[series.iloc[1] - 1, series.iloc[0] - 1] = series.iloc[2]
        npt.assert_array_equal(X, array)

    def test_n_genes_n_cells(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data/10x/hg19/matrix.mtx")
        loader = get_data_loader(file_name)
        self.assertEqual(loader.n_genes, loader.n_cols)
        self.assertEqual(loader.n_cells, loader.n_rows)