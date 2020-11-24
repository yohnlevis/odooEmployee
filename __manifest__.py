# -*- coding: utf-8 -*-


{
    'name': 'Controlemployees',
    'version': '12.0.1.0.1',
    'summary': 'Modulo para controlar el horario laboral de empleados',
    'category': 'Empleados',
    'author': 'Yohn Levis',
    'maintainer': 'Yohn levis',
    'company': 'Universidad de Manizales',
    'website': 'https://www.umanizales.edu.co',
    'data': [  #Para importar los archivos que sean de vistas o de seguridad.
       # 'views/product_label.xml',
    'views/controlemployees_registro_view.xml',
    'views/controlemployees_menu.xml',
    'security/controlemployees_security.xml',
    'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
