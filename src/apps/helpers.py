from datetime import datetime


def save_company_image(instance, filename):
    """path store companies' images"""
    date = datetime.now()  # get current date
    username = instance.name  # get the company's name
    year = date.year
    month = date.month
    day = date.day
    # save user images to images/ with their name
    # as the name of the folder.
    return f'images/{username}/{year}/{month}/{day}/{filename}'
