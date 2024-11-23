"""
Module de gestion des erreurs pour le jeu Quixo.

Cette classe définit une exception personnalisée utilisée pour signaler les erreurs spécifiques 
qui peuvent survenir lors de l'exécution du jeu Quixo.

Attributes:
    None: Il n'y a pas d'attributs spécifiques pour cette classe.

Functions:
    QuixoError: Exception personnalisée pour signaler des erreurs spécifiques dans le jeu Quixo.
"""

class QuixoError(Exception):
    """
    Exception personnalisée pour signaler des erreurs dans le jeu Quixo.

    Args:
        message (str): Message d'erreur à afficher. Par défaut, un message générique
            est fourni si aucun message spécifique n'est passé.

    Raises:
        QuixoError: Lève une exception avec un message d'erreur fourni ou par défaut.

    Returns:
        None: La classe ne retourne rien, elle sert uniquement à signaler des erreurs spécifiques.
    """
    
    def __init__(self, message="Une erreur est survenue dans le jeu Quixo."):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Message d'erreur. Si aucun message n'est fourni, un message par défaut
                est utilisé.

        """
        super().__init__(message)
