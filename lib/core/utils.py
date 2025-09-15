import numpy as np
import time
import pandas as pd

class Utils:
    
    @staticmethod
    def frequence(n):
        """
            The probability of excess (non-exceedance) frequence
        """
        return (np.arange(1, n+1) - 0.5) / n
    
    @staticmethod
    def gumbel_var(freq):
        """
        """
        return - np.log(-np.log(freq))
    
    @staticmethod
    def sleep(duration: float = 1):
        """_summary_

        Args:
            duration (float): _description_
        """
        time.sleep(duration)
    
    # @staticmethod
    # def transform_to_hourly_excel(input_file_path):
    #     """
    #     Transforme un fichier de données horaires en un fichier Excel structuré.

    #     Le script effectue les opérations suivantes :
    #     1.  Charge les données depuis un fichier CSV ou Excel.
    #     2.  "Dépivote" les colonnes de jours (01, 02, ..., 31) pour créer une structure "longue".
    #     3.  Crée une colonne de date et heure complète (DateTime) pour chaque enregistrement.
    #     4.  Pivote le tableau pour obtenir les dates/heures en lignes et les noms des stations en colonnes.
    #     5.  Sauvegarde le DataFrame résultant dans un fichier Excel (.xlsx).

    #     Args:
    #         input_file_path (str): Le chemin vers votre fichier d'entrée au format CSV, XLS ou XLSX.
            
    #     """
    #     try:
    #         # --- Étape 1: Charger le fichier de données ---
    #         # Déterminer le type de fichier et charger en conséquence
    #         file_extension = input_file_path.lower().split('.')[-1]
            
    #         if file_extension == 'csv':
    #             # Pour les fichiers CSV, essayer différents encodages
    #             try:
    #                 df = pd.read_csv(input_file_path, encoding='utf-8')
    #             except UnicodeDecodeError:
    #                 try:
    #                     df = pd.read_csv(input_file_path, encoding='latin-1')
    #                 except UnicodeDecodeError:
    #                     df = pd.read_csv(input_file_path, encoding='cp1252')
    #         elif file_extension in ['xls', 'xlsx']:
    #             # Pour les fichiers Excel
    #             df = pd.read_excel(input_file_path)
    #         else:
    #             raise ValueError(f"Format de fichier non supporté: {file_extension}. Utilisez .csv, .xls ou .xlsx")

    #         # Identifier les colonnes de jours (celles qui sont des chiffres).
    #         day_cols = [col for col in df.columns if col.isdigit()]
            
    #         # --- Étape 2: Dépivoter les colonnes de jours ---
    #         # Transforme les colonnes '01', '02', etc., en une seule colonne 'Day'.
    #         id_vars = [col for col in df.columns if not col.isdigit()]
    #         df_melted = pd.melt(df, id_vars=id_vars, var_name='Day', value_name='Pluie_mm')

    #         # --- Étape 3: Créer une colonne DateHeure complète ---
    #         # Assurer que les types de données sont corrects avant de combiner.
    #         df_melted['Day'] = df_melted['Day'].astype(str).str.zfill(2) # Assure le format '01', '02'...
    #         df_melted['Month'] = df_melted['Month'].astype(str).str.zfill(2)
    #         df_melted['Year'] = df_melted['Year'].astype(str)
            
    #         # Combiner Année, Mois, Jour et Heure pour créer un horodatage complet.
    #         # Le format de la colonne 'Time' est déjà 'HH:MM', donc on peut le concaténer.
    #         datetime_str = df_melted['Year'] + '-' + df_melted['Month'] + '-' + df_melted['Day'] + ' ' + df_melted['Time']
            
    #         # Convertir la chaîne en un vrai objet datetime.
    #         # errors='coerce' transformera les dates/heures invalides (ex: 31 Février) en NaT (Not a Time).
    #         df_melted['DateHeure'] = pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M', errors='coerce')

    #         # Supprimer les lignes avec des dates invalides (créées par 'coerce').
    #         df_melted.dropna(subset=['DateHeure'], inplace=True)
            
    #         # --- Étape 4: Pivoter le tableau pour le format final ---
    #         # Met les horodatages comme index, les noms de station comme colonnes
    #         # et les précipitations horaires comme valeurs.
    #         # On utilise pivot_table au cas où il y aurait des doublons (même station, même heure).
    #         df_final = df_melted.pivot_table(index='DateHeure', columns='Name', values='Pluie_mm', aggfunc='sum')
            
    #         # Trier l'index pour s'assurer que les dates/heures sont dans l'ordre chronologique.
    #         df_final.sort_index(inplace=True)

    #         # --- Étape 5: Sauvegarder le fichier au format Excel ---
    #         # Utilise le moteur 'openpyxl' pour écrire le fichier .xlsx.
    #         # df_final.to_excel(output_file_path, engine='openpyxl')

    #         # print(f"La transformation est terminée. Le fichier Excel a été sauvegardé ici : {output_file_path}")

    #     except FileNotFoundError:
    #         print(f"Erreur: Le fichier d'entrée '{input_file_path}' n'a pas été trouvé.")
    #     except Exception as e:
    #         print(f"Une erreur inattendue est survenue: {e}")
            
    #     return df_final  # Retourne le DataFrame final pour utilisation
    
    @staticmethod
    def convert_to_cdt_hourly(file_path, date_format="%Y-%m-%d %H:%M:%S"):
        # Charger données
        
        try:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Format de fichier non supporté. Utilisez .csv, .xls ou .xlsx")
            
            # Colonnes de jours (01, 02, ...)
            day_cols = [str(i).zfill(2) for i in range(1, 32) if str(i).zfill(2) in df.columns]
            # print(f"Colonnes jours détectées : {day_cols}")

            # Mettre en format long
            df_long = df.melt(
                id_vars=["Name", "Geogr1", "Geogr2", "Year", "Month", "Time"],
                value_vars=day_cols,
                var_name="Day",
                value_name="Value"
            )

            # Construire DateTime : YYYYMMDDHHMM
            df_long["Day"] = df_long["Day"].astype(int)
            df_long["Datetime"] = pd.to_datetime(
                df_long[["Year", "Month", "Day"]].astype(str).agg("-".join, axis=1)
                + " " + df_long["Time"].astype(str),
                format="%Y-%m-%d %H:%M",
                errors="coerce"
            )

            # Supprimer les datetime invalides
            df_long = df_long.dropna(subset=["Datetime"])

            # Formater en CDT : 
            # df_long["Datetime"] = df_long["Datetime"].dt.strftime(date_format)

            df_cdt = df_long.pivot_table(
                index="Datetime", columns="Name", values="Value"
            )

            # Ajouter coordonnées en 2 premières lignes
            # coords = df_long.drop_duplicates("Name")[["Name", "Geogr1", "Geogr2"]]
            # lon_line = coords.set_index("Name")["Geogr1"]
            # lat_line = coords.set_index("Name")["Geogr2"]

            # df_cdt = pd.concat([lon_line.to_frame().T, lat_line.to_frame().T, df_cdt])

            # Sauvegarder
            # df_cdt.to_csv(output_path, sep="\t", index=True)
            # Générer l’index horaire complet
            full_index = pd.date_range(start=df_cdt.index.min(),
                                    end=df_cdt.index.max(),
                                    freq="h")

            # Réindexer la série
            df_cdt = df_cdt.reindex(full_index)


            return df_cdt
            
        except FileNotFoundError:
            print(f"Erreur: Le fichier d'entrée '{file_path}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur inattendue est survenue: {e}")


    @staticmethod
    def calculate_annual_max_rainfall(df_hourly, windows):
        """
        Calcule les précipitations maximales annuelles pour différentes durées.

        Args:
            df_hourly (pandas.DataFrame): Le DataFrame contenant les données horaires.

        Returns:
            dict: Un dictionnaire où les clés sont les noms des stations et les valeurs
                sont les DataFrames des pluies maximales annuelles correspondants.
                Retourne None en cas d'erreur.
        """
        if df_hourly is None:
            return None
            
        try:
            # print("\nÉtape 2: Calcul des précipitations maximales annuelles...")
            stations = df_hourly.columns
            
            # Dictionnaire qui contiendra tous les résultats
            analysis_dict = {}

            for station in stations:
                # print(f"  - Traitement de la station : {station}")
                station_data = df_hourly[station].copy()
                # station_data['Year'] = station_data.index.year
                
                #creation d'un DataFrame vide
                df = pd.DataFrame()
                
                for w in windows:
                    df[w] = station_data.rolling(pd.Timedelta(w, "h"), center=True).sum() / w
                    
                
                # Ajout du DataFrame de la station au dictionnaire final
                analysis_dict[station] = df.resample('YE').max()
                
                # Affichage des années supprimées
                removed_years = analysis_dict[station].index[analysis_dict[station].isna().any(axis=1)].unique()
                
                if len(removed_years) > 0:
                    # print(f"  - Années supprimées pour {station} : {removed_years}")
                    pass
                
                # Supprimer les années (lignes) ayant une valeur NaN
                analysis_dict[station].dropna(inplace=True)
                
                

            # print(" -> Calcul terminé.")
            return analysis_dict

        except Exception as e:
            print(f"Une erreur est survenue lors du calcul des maximums annuels: {e}")
            raise e