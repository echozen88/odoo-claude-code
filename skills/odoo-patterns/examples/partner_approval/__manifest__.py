# -*- coding: utf-8 -*-
# Part of Odoo Claud Code - Partner Approval State Module
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Approval State',
    'version': '19.0.1.0.0',
    'category': 'Base',
    'summary': 'Adds approval state field to res.partner for tracking supplier and customer approval status',
    'description': """
    This module adds an approval state field to the res.partner model for tracking the approval
    status of suppliers and customers. It provides:

    Features
    --------
    - Approval state field (draft, pending, approved, rejected)
    - Approval workflow
    - Approval history
    - Approval dashboard
    """,
    'author': 'Odoo Claud Code Team',
    'website': 'https://github.com/echozen88/odoo-claude-code',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/partner_views.xml',
        'views/menu.xml',
        'views/approval_dashboard.xml',
        'views/approval_history.xml',
        'data/approval_states.xml',
        'i18n/zh_CN.po',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}