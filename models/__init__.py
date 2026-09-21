# -*- coding: utf-8 -*-
# Même principe que le __init__.py racine, mais pour le dossier models/.
# Chaque fichier Python de modèle doit être importé ici pour être chargé par Odoo.
# L'ordre n'a pas d'importance en général, sauf si un modèle référence un autre
# dans sa définition (rare).

from . import library_author
from . import library_category
from . import library_book