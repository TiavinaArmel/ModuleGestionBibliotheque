# -*- coding: utf-8 -*-
"""
Modèle Catégorie.

Une catégorie regroupe des livres par thème (Roman, Science-fiction...).
Plusieurs livres peuvent partager la même catégorie.
C'est une relation simple Many2one / One2many comme Auteur / Livres.
"""

from odoo import models, fields


class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = "Catégorie de livre"
    _order = 'name asc'

    # Champ affiché par défaut.
    name = fields.Char(string="Nom", required=True)

    # Description courte.
    description = fields.Text(string="Description")

    # Relation inverse : tous les livres de cette catégorie.
    # Le champ inverse côté livre s'appellera "category_id".
    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='category_id',
        string="Livres"
    )

    # Champ calculé pour compter les livres.
    book_count = fields.Integer(
        string="Nombre de livres",
        compute='_compute_book_count'
    )

    def _compute_book_count(self):
        for category in self:
            category.book_count = len(category.book_ids)