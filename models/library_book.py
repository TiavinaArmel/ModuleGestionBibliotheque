# -*- coding: utf-8 -*-
"""
Modèle Livre.

C'est le modèle central du module. Un livre est relié à :
- UN auteur (Many2one vers library.author)
- UNE catégorie (Many2one vers library.category)
- PLUSIEURS tags (Many2many vers library.tag — non implémenté ici)

Il possède un workflow simple : draft → published.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = "Livre de bibliothèque"
    _order = 'name asc'

    # ------------------------------------------------------------------
    # CHAMPS SIMPLES
    # ------------------------------------------------------------------

    name = fields.Char(
        string="Titre",
        required=True,
        help="Titre du livre."
    )

    isbn = fields.Char(
        string="ISBN",
        help="Numéro ISBN unique du livre."
    )

    pages = fields.Integer(
        string="Nombre de pages",
        default=0
    )

    publication_date = fields.Date(string="Date de publication")

    # Champ Booléen : disponible ou non.
    available = fields.Boolean(
        string="Disponible",
        default=True
    )

    # Champ Selection : liste fermée de valeurs.
    # Chaque tuple est (valeur_technique, label_affiché).
    # La valeur technique est stockée en base, le label est affiché.
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('published', 'Publié'),
            ('borrowed', 'Emprunté'),
        ],
        string="État",
        default='draft',
        required=True
    )

    # ------------------------------------------------------------------
    # RELATIONS
    # ------------------------------------------------------------------

    # Many2one : "ce livre a UN auteur".
    # Crée une colonne "author_id INTEGER" en base, avec une FOREIGN KEY
    # vers la table library_author.
    author_id = fields.Many2one(
        comodel_name='library.author',
        string="Auteur",
        ondelete='set null'   # Si l'auteur est supprimé, author_id devient NULL.
    )

    # Many2one vers la catégorie.
    category_id = fields.Many2one(
        comodel_name='library.category',
        string="Catégorie",
        ondelete='set null'
    )

    # ------------------------------------------------------------------
    # CONTRAINTES SQL
    # ------------------------------------------------------------------

    # _sql_constraints : liste de tuples (nom, contrainte_sql, message).
    # Ces contraintes sont créées DIRECTEMENT en base PostgreSQL.
    # Elles sont plus performantes que les contraintes Python.
    _sql_constraints = [
        (
            'isbn_unique',                       # Nom interne de la contrainte.
            'UNIQUE(isbn)',                      # Contrainte SQL.
            'L\'ISBN doit être unique !'         # Message d'erreur affiché.
        ),
    ]

    # ------------------------------------------------------------------
    # CONTRAINTES PYTHON
    # ------------------------------------------------------------------

    # @api.constrains : vérifie une règle à chaque create/write.
    # Plus flexible que _sql_constraints mais moins performant.
    # Ici : un livre ne peut pas avoir un nombre de pages négatif.
    @api.constrains('pages')
    def _check_pages(self):
        for book in self:
            if book.pages < 0:
                raise ValidationError("Le nombre de pages ne peut pas être négatif.")

    # ------------------------------------------------------------------
    # MÉTHODES MÉTIER (appelées par des boutons)
    # ------------------------------------------------------------------

    # Convention Odoo : les méthodes appelées par des boutons
    # commencent par "action_". Cela les rend faciles à repérer.
    def action_publish(self):
        """Passe le livre de l'état 'draft' à 'published'."""
        for book in self:
            book.state = 'published'

    def action_draft(self):
        """Remet le livre en brouillon."""
        for book in self:
            book.state = 'draft'

    def action_borrow(self):
        """Marque le livre comme emprunté."""
        for book in self:
            book.state = 'borrowed'
            book.available = False

    def action_return(self):
        """Marque le livre comme retourné (disponible)."""
        for book in self:
            book.state = 'published'
            book.available = True