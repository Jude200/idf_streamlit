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
    
    @staticmethod
    def transform_to_hourly_excel(input_file_path):
        """
        Transforme un fichier de données horaires en un fichier Excel structuré.

        Le script effectue les opérations suivantes :
        1.  Charge les données depuis un fichier CSV ou Excel.
        2.  "Dépivote" les colonnes de jours (01, 02, ..., 31) pour créer une structure "longue".
        3.  Crée une colonne de date et heure complète (DateTime) pour chaque enregistrement.
        4.  Pivote le tableau pour obtenir les dates/heures en lignes et les noms des stations en colonnes.
        5.  Sauvegarde le DataFrame résultant dans un fichier Excel (.xlsx).

        Args:
            input_file_path (str): Le chemin vers votre fichier d'entrée au format CSV, XLS ou XLSX.
            
        """
        try:
            # --- Étape 1: Charger le fichier de données ---
            # Déterminer le type de fichier et charger en conséquence
            file_extension = input_file_path.lower().split('.')[-1]
            
            if file_extension == 'csv':
                # Pour les fichiers CSV, essayer différents encodages
                try:
                    df = pd.read_csv(input_file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(input_file_path, encoding='latin-1')
                    except UnicodeDecodeError:
                        df = pd.read_csv(input_file_path, encoding='cp1252')
            elif file_extension in ['xls', 'xlsx']:
                # Pour les fichiers Excel
                df = pd.read_excel(input_file_path)
            else:
                raise ValueError(f"Format de fichier non supporté: {file_extension}. Utilisez .csv, .xls ou .xlsx")

            # Identifier les colonnes de jours (celles qui sont des chiffres).
            day_cols = [col for col in df.columns if col.isdigit()]
            
            # --- Étape 2: Dépivoter les colonnes de jours ---
            # Transforme les colonnes '01', '02', etc., en une seule colonne 'Day'.
            id_vars = [col for col in df.columns if not col.isdigit()]
            df_melted = pd.melt(df, id_vars=id_vars, var_name='Day', value_name='Pluie_mm')

            # --- Étape 3: Créer une colonne DateHeure complète ---
            # Assurer que les types de données sont corrects avant de combiner.
            df_melted['Day'] = df_melted['Day'].astype(str).str.zfill(2) # Assure le format '01', '02'...
            df_melted['Month'] = df_melted['Month'].astype(str).str.zfill(2)
            df_melted['Year'] = df_melted['Year'].astype(str)
            
            # Combiner Année, Mois, Jour et Heure pour créer un horodatage complet.
            # Le format de la colonne 'Time' est déjà 'HH:MM', donc on peut le concaténer.
            datetime_str = df_melted['Year'] + '-' + df_melted['Month'] + '-' + df_melted['Day'] + ' ' + df_melted['Time']
            
            # Convertir la chaîne en un vrai objet datetime.
            # errors='coerce' transformera les dates/heures invalides (ex: 31 Février) en NaT (Not a Time).
            df_melted['DateHeure'] = pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M', errors='coerce')

            # Supprimer les lignes avec des dates invalides (créées par 'coerce').
            df_melted.dropna(subset=['DateHeure'], inplace=True)
            
            # --- Étape 4: Pivoter le tableau pour le format final ---
            # Met les horodatages comme index, les noms de station comme colonnes
            # et les précipitations horaires comme valeurs.
            # On utilise pivot_table au cas où il y aurait des doublons (même station, même heure).
            df_final = df_melted.pivot_table(index='DateHeure', columns='Name', values='Pluie_mm', aggfunc='sum')
            
            # Trier l'index pour s'assurer que les dates/heures sont dans l'ordre chronologique.
            df_final.sort_index(inplace=True)

            # --- Étape 5: Sauvegarder le fichier au format Excel ---
            # Utilise le moteur 'openpyxl' pour écrire le fichier .xlsx.
            # df_final.to_excel(output_file_path, engine='openpyxl')

            # print(f"La transformation est terminée. Le fichier Excel a été sauvegardé ici : {output_file_path}")

        except FileNotFoundError:
            print(f"Erreur: Le fichier d'entrée '{input_file_path}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur inattendue est survenue: {e}")
            
        return df_final  # Retourne le DataFrame final pour utilisation

    @staticmethod
    def calculate_annual_max_rainfall(df_hourly):
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
            print("\nÉtape 2: Calcul des précipitations maximales annuelles...")
            stations = df_hourly.columns
            windows = [1, 2, 3, 6, 12, 24]
            
            # Dictionnaire qui contiendra tous les résultats
            analysis_dict = {}

            for station in stations:
                print(f"  - Traitement de la station : {station}")
                station_data = df_hourly[[station]].copy()
                station_data['Year'] = station_data.index.year
                
                results_station = []
                for year in sorted(station_data['Year'].unique()):
                    data_year = station_data[station_data['Year'] == year][station]
                    max_values_for_year = {'Année': year}
                    for w in windows:
                        rolling_sum = data_year.rolling(window=w, min_periods=1).sum()
                        max_values_for_year[f'{w}h'] = rolling_sum.max()
                    results_station.append(max_values_for_year)

                df_results = pd.DataFrame(results_station).set_index('Année')
                
                # Ajout du DataFrame de la station au dictionnaire final
                analysis_dict[station] = df_results
            
            print(" -> Calcul terminé.")
            return analysis_dict

        except Exception as e:
            print(f"Une erreur est survenue lors du calcul des maximums annuels: {e}")
            return None