# -*- coding: utf-8 -*-
"""
Modèle Auteur.

Un auteur est une entité indépendante : il a un nom, une nationalité,
une biographie. Plusieurs livres peuvent être écrits par le même auteur,
donc la relation est "un auteur → plusieurs livres".

C'est le modèle "parent" dans la relation Many2one / One2many.
"""

from odoo import models, fields, api


class LibraryAuthor(models.Model):
    # _name : identifiant technique du modèle, unique dans tout Odoo.
    # La convention est "nom_module.entite" mais tout identifiant en
    # snake_case avec un point fonctionne.
    # Odoo crée automatiquement la table PostgreSQL "library_author".
    _name = 'library.author'

    # _description : description lisible, OBLIGATOIRE en Odoo 10.
    _description = "Auteur de livre"

    # _order : tri par défaut quand on liste les auteurs.
    # Sans ce champ, Odoo trie par "id" (ordre de création), ce qui
    # n'est pas toujours pertinent.
    _order = 'name asc'

    # ------------------------------------------------------------------
    # CHAMPS SIMPLES
    # ------------------------------------------------------------------

    # "name" est un champ SPÉCIAL dans Odoo : c'est l'affichage par défaut
    # d'un enregistrement. Quand Odoo doit afficher un auteur sous forme
    # de texte (dans un Many2one, un breadcrumb...), il utilise ce champ.
    name = fields.Char(
        string="Nom complet",        # Label affiché dans l'interface.
        required=True,               # Obligatoire (NOT NULL en SQL).
        help="Nom et prénom de l'auteur."
    )

    # Champ texte simple pour la nationalité.
    nationality = fields.Char(string="Nationalité")

    # Champ texte long (pas de limite) pour la biographie.
    # Différence avec Char : Char = VARCHAR court, Text = TEXT illimité.
    biography = fields.Text(string="Biographie")

    # Champ date pour la date de naissance.
    birth_date = fields.Date(string="Date de naissance")

    # ------------------------------------------------------------------
    # RELATIONS
    # ------------------------------------------------------------------

    # One2many : "un auteur a plusieurs livres".
    # IMPORTANT : ce champ ne crée AUCUNE colonne en base.
    # C'est la vue inversée d'un Many2one défini dans library.book.
    #
    # Paramètres :
    #   'library.book'  → le modèle cible (le "plusieurs" côté)
    #   'author_id'     → le nom du champ Many2one DANS library.book
    #                     qui pointe vers cet auteur
    #
    # En clair : "donne-moi tous les library.book dont author_id = moi".
    book_ids = fields.One2many(
        comodel_name='library.book',   # Modèle cible.
        inverse_name='author_id',      # Champ inverse dans le modèle cible.
        string="Livres écrits"
    )

    # ------------------------------------------------------------------
    # CHAMPS CALCULÉS
    # ------------------------------------------------------------------

    # Un champ calculé n'est PAS stocké en base par défaut (store=False).
    # Il est recalculé à la volée à chaque lecture.
    # Ici : on veut compter combien de livres a écrit l'auteur.
    book_count = fields.Integer(
        string="Nombre de livres",
        compute='_compute_book_count',  # Nom de la méthode de calcul.
        store=False                     # Non stocké = recalculé à chaque lecture.
    )

    # @api.depends : décorateur Odoo qui dit "recalcule ce champ quand
    # les champs listés changent". Sans ce décorateur, Odoo ne saurait
    # pas quand recalculer.
    @api.depends('book_ids')
    def _compute_book_count(self):
        # Convention : les méthodes de calcul commencent par "_compute_".
        # Comme toujours, self est un recordset : on itère.
        for author in self:
            # len() d'un recordset = nombre d'enregistrements.
            author.book_count = len(author.book_ids)