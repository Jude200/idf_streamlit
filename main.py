# import numpy as np

# from lib.core.idf import IDF


# data_path = "data/data.csv"

# idf = IDF(data_path=data_path, return_periods = np.array([2, 5, 10, 20, 50, 100]))

# print(idf.montana_estimator)
import numpy as np

from lib.core.utils import Utils
from lib.core.idf import IDF

data_path = r"C:\Jude_Seruch\unstim\ensgmm_3\stage_meteo\climatologies_changements_climatiques\python_code\idf\data\DONNEES_FUSTEL.xls"

# data_path = r"C:\Jude_Seruch\unstim\ensgmm_3\stage_meteo\climatologies_changements_climatiques\python_code\idf\data\DONNEES_PLUIE_HORAIRE_2006_2024.xls"

print("Loading data...")

idf = IDF(data_path=data_path, return_periods = np.array([5, 10, 20, 50, 100]), windows=np.array([1, 2, 4, 8, 24]))
print(idf.dfs)

# print(idf.montana_estimator)

