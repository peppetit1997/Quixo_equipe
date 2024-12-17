from quixo import Quixo

class QuixoIA(Quixo):
    def __init__(self):
        super().__init__()

    def lister_les_coups_possibles(self, plateau, cube):
        """Liste tous les coups possibles pour le joueur.

        Args:
            plateau (list[list[str]]): Le plateau de jeu sous forme de grille 5x5.
            cube (str): Le symbole du joueur ('X' ou 'O').

        Returns:
            list[dict]: Une liste de dictionnaires représentant les coups possibles.
        """
        # Créer la liste des coups possibles
        Coups_possibles = []
    
        # Créer une liste pour les coordonnées disponibles sur les bords
        Coordonnees_disponibles = []

        # Parcourir les bords pour trouver les cubes jouables
        for x in range(5):
            for y in range(5):
                # Vérifier si la case est sur un bord
                if x in [1, 5] or y in [1, 5]:
                    # Ajouter la case si elle est vide ou contient le symbole du joueur
                    if plateau[x][y] == "" or plateau[x][y] == cube:
                        Coordonnees_disponibles.append((x, y))

        # Générer les coups possibles pour chaque coordonnée disponible
        for (x, y) in Coordonnees_disponibles:
            # Vérifier les directions possibles selon la position
            if x > 0:  # Peut aller vers le haut
                Coups_possibles.append({"origine": [x, y], "direction": "haut"})
            if x < 5:  # Peut aller vers le bas
                Coups_possibles.append({"origine": [x, y], "direction": "bas"})
            if y > 0:  # Peut aller à gauche
                Coups_possibles.append({"origine": [x, y], "direction": "gauche"})
            if y < 5:  # Peut aller à droite
                Coups_possibles.append({"origine": [x, y], "direction": "droite"})

        return Coups_possibles

        
    def analyser_le_plateau(self):
        """Analyse l'état actuel du plateau."""
        pass

    def partie_terminée(self):
        """Détermine si la partie est terminée et retourne le résultat."""
        pass

    def trouver_un_coup_vainqueur(self):
        """Trouve un coup permettant de gagner la partie."""
        pass

    def trouver_un_coup_bloquant(self):
        """Trouve un coup permettant de bloquer l'adversaire."""
        pass

    def jouer_un_coup(self):
        """Joue un coup en fonction de la stratégie."""
        pass
