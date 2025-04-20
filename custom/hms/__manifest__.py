{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'category': 'Healthcare',
    'author': 'Your Name',
    'depends': ['base'],
    'description': """
        Hospital management system module.
    """,
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'reports/report.xml',
        'reports/patient_report_template.xml',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/department_views.xml',
        'views/customer_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}