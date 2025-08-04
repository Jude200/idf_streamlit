# import numpy as np

# from lib.core.idf import IDF


# data_path = "data/data.csv"

# idf = IDF(data_path=data_path, return_periods = np.array([2, 5, 10, 20, 50, 100]))

# print(idf.montana_estimator)

from lib.core.utils import Utils

data_path = "data/DONNEES_PLUIE_HORAIRE_2006_2024.xls"

df = Utils.transform_to_hourly_excel(input_file_path=data_path)

print(df.head())

sdf = Utils.calculate_annual_max_rainfall(df_hourly=df)

print(sdf)