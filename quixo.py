"""Module Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * QuixoError - Classe d'erreur pour le jeu Quixo.

Functions:
    * interpréter_la_commande - Génère un interpréteur de commande.
"""

import argparse

from quixo_error import QuixoError

from plateau import Plateau


class Quixo:
    """Classe principale du jeu Quixo.
    
    Cette classe gère l'état du jeu et les interactions avec le plateau.
    """

    def __init__(self, joueurs, plateau=None) -> None:
        """Constructeur de la classe Quixo

        Vous ne devez rien modifier dans cette méthode.

        Args:
            joueurs (list[str]): La liste des deux joueurs.
                Le premier joueur possède le symbole "X" et le deuxième "O".
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.joueurs = joueurs
        self.plateau = Plateau(plateau)

    def état_partie(self):
        """Retourne une copie du jeu

        Retourne une copie du jeu pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            dict: La représentation du jeu tel que retourné par le serveur de jeu.
        """
        return {
            "joueurs": self.joueurs,
            "plateau": self.plateau.état_plateau(),
        }

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de la partie

        Déplacer le code de vos fonctions formater_légende et formater_jeu ici.
        Adaptez votre code en conséquence et faites appel à Plateau
        pour obtenir la représentation du plateau.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        entete = (
    "Légende:\n"
    f"   X={self.joueurs[0]}\n"
    f"   O={self.joueurs[1]}\n"
)

        return entete + str(self.plateau)

    def déplacer_pion(self, pion, origine, direction):
        """Déplacer un pion dans une direction donnée.

        Applique le changement au Plateau de jeu

        Args:
            pion (str): Le pion à déplacer, soit "X" ou "O".
            origine (list[int]): La position (x, y) du pion sur le plateau.
            direction (str): La direction du déplacement, soit "haut", "bas", "gauche" ou "droite".
        """
        if pion not in ["X", "o"]:
            raise QuixoError("Le pion doit etre 'X' ou 'O'.")
        if direction not in ["haut", "bas", "gauche", "droite"]:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        x, y = origine


        if direction == "haut":
            nouvelle_position = [x - 1, y]
        elif direction == "bas":
            nouvelle_position = [x + 1, y]
        elif direction == "gauche":
            nouvelle_position = [x, y - 1]
        elif direction == "droite":
            nouvelle_position = [x, y + 1]

        if not (1 <= nouvelle_position[0] <= 5 and 1 <= nouvelle_position[1] <= 5):
            raise QuixoError("La nouvelle position est hors limites.")

        self.plateau[origine] = " "
        self.plateau.insérer_un_cube(pion, nouvelle_position, direction)


    def choisir_un_coup(self):
        """Demander le prochain coup à jouer au joueur.

        Déplacer le code de votre fonction récupérer_le_coup ici et ajuster le en conséquence.
        Vous devez maintenant valider les entrées de l'utilisateur.

        Returns:
            tuple: Tuple de 2 éléments composé de l'origine du bloc à déplacer et de sa direction.
                L'origine est une liste de 2 entiers [x, y].
                La direction est une chaîne de caractères.

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".

        Examples:
            Donnez la position d'origine du bloc (x,y) :
            Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') :
        """
        try:
            x = int(input("Donnez la position d'origine du bloc (x, y):\nx = "))
            y = int(input("y = "))

            if not (1 <= x <= 5 and 1 <= y <= 5):
                raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

            origine = [x, y]

            direction = input(
                "Quelle direction voulez-vous insérer? "
                "('haut', 'bas', 'gauche', 'droite'):\n"
            )

            if direction not in ["haut", "bas", "gauche", "droite"]:
                raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

            return (origine, direction)

        except ValueError as exc:
            raise QuixoError("Les positions x et y doivent être des entiers.") from exc


def interpréter_la_commande():
    """Génère un interpréteur de commande.
    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
            Cet objet aura l'attribut «idul» représentant l'idul du joueur.
    """
    parser = argparse.ArgumentParser(description='Quixo')
    parser.add_argument("idul", help="IDUL du joueur (Identifiant unique de l'université Laval)")
    parser.add_argument('-a', '--autonome', action='store_true', help='jouer de façon autonome')
    return parser.parse_args()