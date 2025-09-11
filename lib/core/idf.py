from logging import Logger
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from scipy.stats import linregress

from lib.const import *
from lib.core.utils import Utils


class IDF:
    """
    Classe pour l'analyse des courbes IDF (Intensité-Durée-Fréquence) des précipitations.
    
    Cette classe permet de :
    - Charger des données de précipitations maximales annuelles
    - Calculer les paramètres de la distribution de Gumbel
    - Estimer les lames précipitées et intensités pour différentes périodes de retour
    - Calculer les paramètres de Montana pour la modélisation IDF
    
    Attributes:
        data_path (str): Chemin vers le fichier de données
        return_periods (np.ndarray): Périodes de retour à analyser (en années)
        logger (Logger, optional): Logger pour les messages informatifs
        df (pd.DataFrame): Données chargées depuis le fichier
        columns (pd.Index): Colonnes des durées (en heures)
        summary (pd.DataFrame): Statistiques descriptives et paramètres de Gumbel
        rain_estimator (pd.DataFrame): Lames précipitées estimées
        intensity_estimator (pd.DataFrame): Intensités pluviométriques estimées
        montana_params (pd.DataFrame): Paramètres a et b de Montana
        montana_estimator (pd.DataFrame): Intensités estimées par Montana
    """
    
    def __init__(self, data_path: str, return_periods: np.ndarray, logger: Logger = None):
        """
        Initialise une instance IDF et exécute toute la chaîne de traitement.
        
        Args:
            data_path (str): Chemin vers le fichier Excel ou CSV contenant les données
            return_periods (np.ndarray): Périodes de retour à analyser (ex: [2, 5, 10, 25, 50, 100])
            logger (Logger, optional): Logger pour tracer les opérations. Defaults to None.
            
        Raises:
            Exception: Si le fichier n'est pas supporté ou mal formaté
        """
        # Initialisation des attributs principaux
        self.data_path = data_path
        self.return_periods = return_periods
        self.logger = logger
        
        # Initialisation des attributs de données
        self.dfs = {}  # Dictionnaire pour stocker les DataFrames par station
        self.columns = None
        self.stations = None
        self.df = None
        
        # Chargement et validation des données
        self._load_dataframe()
          
        # Calcul des statistiques et paramètres de Gumbel
        self.summary = None
        # self._summary()
        
        # Estimation des lames précipitées
        self.rain_estimator = None
        # self._rain_estimator()
        
        # Calcul des intensités pluviométriques
        self.intensity_estimator = None
        # self._intensity_estimator()
    
        # Calcul des paramètres de Montana
        self.montana_params = None
        # self._montana_parameters()
        
        # Estimation finale avec la formule de Montana
        self.montana_estimator = None
        # self._montana_estimation()
        
        # Le message de succès sera affiché seulement après l'analyse complète
    
    def _load_dataframe(self):
        """
        Charge et valide les données de précipitations depuis un fichier Excel ou CSV.
        
        Le fichier doit contenir :
        - Une colonne 'Year' avec les années
        - Des colonnes numériques représentant les durées en heures (1, 2, 3, 6, 12, 24, etc.)
        - Les valeurs de précipitations maximales annuelles pour chaque durée
        
        Raises:
            Exception: Si le type de fichier n'est pas supporté
            Exception: Si la colonne 'Year' est manquante
            Exception: Si les colonnes de durée ne sont pas des entiers positifs
        """
        try :
            
            df_final = Utils.transform_to_hourly_excel(input_file_path=self.data_path)
            # print(df_final.head())
            
            if df_final is None or df_final.empty:
                raise Exception("Le DataFrame est vide ou mal formaté.")
            
            # print(df_final.columns.tolist())
            
            self.stations = df_final.columns.tolist()

            self.dfs = Utils.calculate_annual_max_rainfall(df_hourly=df_final, windows=[1, 2, 3, 6, 12, 24])
            
            # Première station pour initialiser les attributs
            first_station = next(iter(self.dfs))
            self.columns = self.dfs[first_station].columns
            # print("Colonnes de durée détectées :", self.columns.tolist())
            # print(self.dfs[first_station].head())
            # print(self.dfs[first_station].columns)
            # print(self.columns)
            
        except Exception as e:
            error_msg = f"Erreur lors du chargement des données: {str(e)}"
            if self.logger:
                self.logger.error(error_msg)
            raise Exception(error_msg)
        
        if self.logger:
            stations_str = ", ".join(self.stations[:3])  # Affiche les 3 premières stations
            more_stations = f" et {len(self.stations)-3} autres" if len(self.stations) > 3 else ""
            self.logger.info(f"✅ Fichier traité : {len(self.dfs)} stations ({stations_str}{more_stations}), {len(self.columns)} durées disponibles")

    def do_analysis(self, station: str):
        """
        Exécute l'analyse IDF complète.
        
        Cette méthode est appelée après l'initialisation pour lancer le processus d'analyse.
        Elle appelle les méthodes internes pour calculer les statistiques, estimer les lames,
        intensités et paramètres de Montana.
        """
        if self.logger:
            self.logger.info(f"🚀 Début de l'analyse IDF pour la station: {station}")
        
        # Vérification de la validité de la station
        if station not in self.dfs:
            raise ValueError(f"La station '{station}' n'existe pas dans les données.")
        
        # Sélection des données pour la station
        self.df = self.dfs[station]
        # self.columns = self.df.columns[1:]
        self.columns = self.df.columns
            
        # Calcul des statistiques descriptives et paramètres de Gumbel
        self._summary()
        
        # Estimation des lames précipitées
        self._rain_estimator()
        
        # Calcul des intensités pluviométriques
        self._intensity_estimator()
        
        # Calcul des paramètres de Montana
        self._montana_parameters()
        
        # Estimation finale avec la formule de Montana
        self._montana_estimation()
        
        if self.logger:
            self.logger.info(f"✅ Analyse IDF terminée avec succès pour la station '{station}'")
    
    def _summary(self):
        """
        Calcule les statistiques descriptives et les paramètres de la distribution de Gumbel.
        
        Pour chaque durée de précipitation, cette méthode calcule :
        - La moyenne des précipitations maximales annuelles
        - La variance des précipitations maximales annuelles  
        - Les paramètres mu et beta de la distribution de Gumbel
        
        La distribution de Gumbel est utilisée pour modéliser les valeurs extrêmes de précipitations.
        Les paramètres sont calculés par la méthode des moments :
        - beta = sqrt(6 * variance) / π
        - mu = moyenne - beta * constante_euler_mascheroni
        
        Results:
            self.summary (pd.DataFrame): DataFrame contenant les colonnes Mean, Variance, mu, beta
        """
        if self.logger:
            self.logger.info("📊 Calcul des statistiques et paramètres de Gumbel")
        
        # Sélection des colonnes numériques (durées) en excluant 'Year'
        numeric_columns = self.df.columns
        print(self.df.head())
        # print(numeric_columns)

        # Calcul des statistiques de base pour chaque durée
        mean_values = self.df[numeric_columns].mean()
        variance_values = self.df[numeric_columns].var()
        
        def gumbel_parameters(mean, variance):
            """
            Calcule les paramètres de la distribution de Gumbel par la méthode des moments.
            
            Args:
                mean (float): Moyenne de l'échantillon
                variance (float): Variance de l'échantillon
                
            Returns:
                tuple: (mu, beta) paramètres de position et d'échelle de Gumbel
            """
            # Paramètre d'échelle (beta)
            beta = np.sqrt(6 * variance) / np.pi
            # Paramètre de position (mu) 
            mu = mean - beta * EULER_MASCHERONI
            return mu, beta

        # Calcul des paramètres de Gumbel pour chaque durée
        gumbel_params = {
            col: gumbel_parameters(mean_values[col], variance_values[col]) 
            for col in numeric_columns
        }

        # Création du DataFrame des paramètres de Gumbel
        gumbel_params_df = pd.DataFrame(gumbel_params, index=['mu', 'beta']).T

        # Assemblage du DataFrame de synthèse avec toutes les statistiques
        summary_df = pd.DataFrame({
            'Mean': mean_values,
            'Variance': variance_values
        })
        
        # Concaténation des statistiques de base avec les paramètres de Gumbel
        self.summary = pd.concat([summary_df, gumbel_params_df], axis=1)
        
    
    def _rain_estimator(self):
        """
        Estime les lames précipitées pour chaque durée et période de retour en utilisant la distribution de Gumbel.
        
        Cette méthode applique la formule de quantiles de Gumbel :
        X_T = mu + beta * Y_T
        
        Où :
        - X_T : lame précipitée pour la période de retour T
        - mu, beta : paramètres de Gumbel calculés précédemment
        - Y_T : variable réduite de Gumbel = -ln(-ln(F))
        - F : probabilité de non-dépassement = 1 - 1/T
        
        Results:
            self.rain_estimator (pd.DataFrame): Lames précipitées estimées
                                               Index: durées, Colonnes: périodes de retour
        """
        if self.logger:
            self.logger.info("� Estimation des lames précipitées")
        
        # Calcul de la probabilité de non-dépassement F = 1 - 1/T
        # où T est la période de retour
        F = 1 - 1 / self.return_periods

        # Calcul de la variable réduite de Gumbel Y = -ln(-ln(F))
        gumbel_reduce_var = Utils.gumbel_var(F)

        # Estimation des lames précipitées pour chaque durée
        estimated_rain = {}

        for column in self.columns:
            # Récupération des paramètres de Gumbel pour cette durée
            mu = self.summary.loc[column, 'mu']
            beta = self.summary.loc[column, 'beta']
            
            # Application de la formule de quantile de Gumbel : X = mu + beta * Y
            estimated_rain[column] = mu + beta * gumbel_reduce_var

        # Création du DataFrame avec les durées en index et les périodes de retour en colonnes
        self.rain_estimator = pd.DataFrame(estimated_rain, index=self.return_periods).T

    def _intensity_estimator(self):
        """
        Calcule les intensités pluviométriques à partir des lames précipitées estimées.
        
        L'intensité pluviométrique (mm/h) est obtenue en divisant la lame précipitée (mm)
        par la durée de l'épisode pluvieux (h) :
        
        Intensité = Lame précipitée / Durée
        
        Cette transformation est essentielle pour établir les courbes IDF qui lient
        l'intensité, la durée et la fréquence des précipitations.
        
        Results:
            self.intensity_estimator (pd.DataFrame): Intensités pluviométriques (mm/h)
                                                    Index: durées, Colonnes: périodes de retour
        """
        if self.logger:
            self.logger.info("⚡ Calcul des intensités pluviométriques")
        
        # Calcul des intensités pour chaque durée
        estimated_intensity_rain = {}

        for column in self.columns:
            # Conversion de la durée en entier pour le calcul
            duration_hours = int(column)
            
            # Calcul de l'intensité : lame précipitée / durée
            # self.rain_estimator.loc[column] contient les lames pour toutes les périodes de retour
            estimated_intensity_rain[column] = self.rain_estimator.loc[column] / duration_hours
            
        # Création du DataFrame des intensités avec la même structure que rain_estimator
        self.intensity_estimator = pd.DataFrame(estimated_intensity_rain, index=self.return_periods).T

    def _montana_parameters(self):
        """
        Calcule les paramètres de Montana (a et b) pour chaque période de retour.
        
        La formule de Montana établit une relation puissance entre l'intensité pluviométrique
        et la durée de l'épisode :
        
        I = b * t^(-a)
        
        Où :
        - I : intensité pluviométrique (mm/h)
        - t : durée (h)  
        - a : coefficient d'abattement (sans dimension)
        - b : intensité à 1 heure (mm/h)
        
        Les paramètres sont obtenus par régression linéaire en échelle log-log :
        ln(I) = ln(b) - a * ln(t)
        
        Results:
            self.montana_params (pd.DataFrame): Paramètres a et b pour chaque période de retour
                                              Index: périodes de retour, Colonnes: ['a', 'b']
        """
        if self.logger:
            self.logger.info("🔧 Calcul des paramètres de Montana")
        
        # Transformation logarithmique des durées
        log_hours = np.log(self.columns.astype(float))
        
        # Transformation logarithmique des intensités pour toutes les périodes de retour
        log_intensities = np.log(self.intensity_estimator.astype(float))
        
        montana_parameters = {}
        
        if self.logger:
            self.logger.info("Régression linéaire pour chaque période de retour")
        
        # Calcul des paramètres pour chaque période de retour
        for period in self.return_periods:
            # Régression linéaire sur les données log-log
            # y = ln(I), x = ln(t) => y = intercept + slope * x
            slope, intercept, r_value, p_value, std_err = linregress(
                log_hours, 
                log_intensities[period]
            )
            
            # Conversion vers les paramètres de Montana :
            # ln(I) = ln(b) - a * ln(t) => slope = -a, intercept = ln(b)
            alpha = -slope  # Coefficient d'abattement (a)
            beta = np.exp(intercept)  # Intensité à 1 heure (b)
            r_squared = r_value**2
            
            montana_parameters[period] = {
                'alpha': alpha, 
                'beta': beta,
                'r_squared': r_squared  # Coefficient de détermination pour la qualité de l'ajustement
            }
            
        # Création du DataFrame des paramètres
        montana_parameters_df = pd.DataFrame(montana_parameters).T
        
        # Renommage des colonnes selon la convention standard
        montana_parameters_df.columns = ['a', 'b', 'r²']
        montana_parameters_df.index.name = 'Période de retour (années)'

        self.montana_params = montana_parameters_df

    def _montana_estimation(self):
        """
        Estime les intensités pluviométriques en appliquant la formule de Montana.
        
        Cette méthode utilise les paramètres a et b calculés précédemment pour reconstituer
        les intensités selon la formule :
        
        I(t,T) = b(T) * t^(-a(T))
        
        Où :
        - I(t,T) : intensité pour la durée t et la période de retour T
        - b(T) : paramètre b pour la période de retour T
        - a(T) : paramètre a pour la période de retour T
        - t : durée en heures
        
        Cette estimation permet de valider la qualité de l'ajustement par Montana
        et d'interpoler/extrapoler pour d'autres durées si nécessaire.
        
        Results:
            self.montana_estimator (pd.DataFrame): Intensités estimées par Montana
                                                  Index: durées, Colonnes: périodes de retour
        """
        if self.logger:
            self.logger.info("📈 Génération des courbes IDF finales")
        
        montana_estimated_intensity = {}
        
        # Calcul des intensités pour chaque période de retour
        for period in self.return_periods:
            # Récupération des paramètres de Montana pour cette période de retour
            alpha = self.montana_params.loc[period, 'a']  # Coefficient d'abattement
            beta = self.montana_params.loc[period, 'b']   # Intensité à 1 heure
            
            # Application de la formule de Montana pour chaque durée : I = b * t^(-a)
            intensities = [
                beta * (float(duration) ** (-alpha)) 
                for duration in self.columns
            ]
            
            montana_estimated_intensity[period] = intensities
            
        # Création du DataFrame avec les durées en index et les périodes de retour en colonnes
        self.montana_estimator = pd.DataFrame(
            montana_estimated_intensity, 
            index=self.columns
        )
        self.montana_estimator.index.name = 'Durée (heures)'
        self.montana_estimator.columns.name = 'Période de retour (années)'
    
    def get_intensity(self, duration: float, return_period: float) -> float:
        """
        Calcule l'intensité pluviométrique pour une durée et période de retour données
        en utilisant la formule de Montana.
        
        Args:
            duration (float): Durée de l'épisode pluvieux en heures
            return_period (float): Période de retour en années
            
        Returns:
            float: Intensité pluviométrique en mm/h
            
        Raises:
            ValueError: Si la période de retour n'est pas disponible
        """
        if return_period not in self.return_periods:
            raise ValueError(f"Période de retour {return_period} non disponible. "
                           f"Périodes disponibles: {list(self.return_periods)}")
        
        # Récupération des paramètres de Montana
        alpha = self.montana_params.loc[return_period, 'a']
        beta = self.montana_params.loc[return_period, 'b']
        
        # Application de la formule : I = b * t^(-a)
        intensity = beta * (duration ** (-alpha))
        
        return intensity
    
    def get_rainfall_depth(self, duration: float, return_period: float) -> float:
        """
        Calcule la lame précipitée pour une durée et période de retour données.
        
        Args:
            duration (float): Durée de l'épisode pluvieux en heures
            return_period (float): Période de retour en années
            
        Returns:
            float: Lame précipitée en mm
        """
        intensity = self.get_intensity(duration, return_period)
        rainfall_depth = intensity * duration
            
        return rainfall_depth
    
    def summary_stats(self) -> pd.DataFrame:
        """
        Retourne un résumé des statistiques et paramètres calculés.
        
        Returns:
            pd.DataFrame: Tableau de synthèse avec les statistiques par durée
        """
        return self.summary.copy()
    
    def get_montana_params(self) -> pd.DataFrame:
        """
        Retourne les paramètres de Montana calculés.
        
        Returns:
            pd.DataFrame: Paramètres a, b et r² pour chaque période de retour
        """
        return self.montana_params.copy()
    