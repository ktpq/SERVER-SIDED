from django import template

register = template.Library()

@register.filter
def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections

@register.filter
def formatPhoneNumber(phoneNumber):
    return phoneNumber
    phoneNumber = f"{int(''.join([p for p in phoneNumber if p.isnumeric()])):010d}"
    return f"{phoneNumber[0:3]}-{phoneNumber[3:6]}-{phoneNumber[6:]}"