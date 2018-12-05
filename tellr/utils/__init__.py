from datetime import date

def calculate_age(bday):
    today = date.today()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))