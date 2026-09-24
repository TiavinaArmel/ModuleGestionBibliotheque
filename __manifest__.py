# -*- coding: utf-8 -*-
{
    
    'name': 'Bibliothèque',

    'version': '10.0.1.0.0',

    'summary': 'Gestion simple d\'une bibliothèque (livres, auteurs, catégories).',

    
    'description': """
Module de gestion de bibliothèque.

Fonctionnalités :
- Gestion des livres (titre, auteur, pages, état)
- Gestion des auteurs
- Gestion des catégories
- Workflow simple : brouillon → publié
    """,

    #auteur : Tiavina Armel
    'author': 'Tiavina Armel',
    #le site web du module (optionnel)
    'website': '',
    'category': 'Inventory',
#license du module (LGPL-3, MIT, etc.)
    'license': 'LGPL-3',
#dependance du module (ici, le module "base" d'Odoo)
    'depends': ['base'],

#les données à charger lors de l'installation du module
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_book_view.xml',
        'views/library_author_view.xml',
        'views/library_category_view.xml',
        'views/library_menu.xml',
        'views/library_assets.xml',
        # data livres 
        'data/library_sequence.xml',
        'data/library_author_data.xml',
        'data/library_category_data.xml',
        'data/library_book_data.xml',
    ],

    # Le module peut-il être installé ? (Toujours True en pratique.)
    'installable': True,

    # Le module apparaît-il dans le filtre "Applications" ?
    'application': True,

    # Installer automatiquement à la création de la base ? (False recommandé.)
    'auto_install': False,
}