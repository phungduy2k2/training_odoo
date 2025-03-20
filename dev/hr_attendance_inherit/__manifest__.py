{
    'name': 'HR Attendance Inherit',
    'version': '1.0',
    'category': 'Human Resources/Attendances',
    'summary': 'Module yêu cầu bù công',
    'description': """
        Module cho phép nhân viên tạo yêu cầu chấm công khi quên check-in/check-out
    """,
    'author': "Duypv",
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_attendance_inherit_security.xml',

        'views/hr_attendance_request_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
