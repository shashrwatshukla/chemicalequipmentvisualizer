from PyQt5.QtWidgets import QMessageBox

def format_number(value, decimals=2):
    try:
        return '{:.{}f}'.format(float(value), decimals)
    except:
        return str(value)

def show_error(parent, message):
    QMessageBox.critical(parent, 'Error', str(message))

def show_success(parent, message):
    QMessageBox.information(parent, 'Success', str(message))

def show_question(parent, message):
    reply = QMessageBox.question(parent, 'Confirm', message,
                                 QMessageBox.Yes | QMessageBox.No)
    return reply == QMessageBox.Yes