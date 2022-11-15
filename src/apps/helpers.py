from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import weasyprint
from jinja2 import Environment, FileSystemLoader


class AbstractBasePDFGenerator(ABC):
    """abstract base class for PDFGenerator"""

    @abstractmethod
    def get_parent_directory(self):
        """retrieve parent directory"""
        pass

    @abstractmethod
    def locate_template_path(self):
        """locate the template path"""
        pass

    @abstractmethod
    def locate_static(self):
        """locate the static path and file"""
        pass

    @abstractmethod
    def load_template_path(self):
        """load the template path with jinja2"""
        pass

    @abstractmethod
    def get_template(self):
        """retrieve the template file"""
        pass

    @abstractmethod
    def stringify_context(self):
        """stringify the context and load it in weasyprint for rendering"""
        pass

    @abstractmethod
    def generate_pdf(self):
        """generate pdf from context"""
        pass

    @abstractmethod
    def return_pdf_file_path(self):
        pass

    @abstractmethod
    def delete_pdf(self):
        """delete PDF"""
        pass


class PDFGenerator(AbstractBasePDFGenerator):
    def __init__(self):
        self.data = 'data'
        self.username = 'Admin Customer'

    def get_parent_directory(self):
        parent_directory = Path(__file__).resolve().parent
        return parent_directory

    def locate_template_path(self):
        template_path = f'{self.get_parent_directory()}/templates/pdf'
        return template_path

    def locate_static(self):
        static_path = f'{self.get_parent_directory()}/templates/pdf/pdf.css'
        return static_path

    def load_template_path(self):
        template_path = self.locate_template_path()
        return Environment(loader=FileSystemLoader(template_path))

    def get_template(self):
        return self.load_template_path().get_template('pdf.html')

    def stringify_context(self):
        current_date = datetime.now()

        context = {
            'current_date': current_date.strftime('%Y-%m-%d'),
            'data': self.data,
            'username': self.username,
            'company': 'Alhimaya',
            'category': 'Health',
            'policy': 'Health Insurance',
            'sum_assurance': 20000,
            'tenure': 4,
            'premium': 3,
            'policy_status': 'Approved'
        }
        stringify_context = self.get_template().render(context)
        html = weasyprint.HTML(string=stringify_context)
        return html

    def generate_pdf(self):
        html = self.stringify_context()

        # generate PDF
        return html.write_pdf(f'file_downloads/{self.username}.pdf', stylesheets=[self.locate_static()])

    def return_pdf_file_path(self):
        root_dir = self.get_parent_directory().parent

        # create the file_downloads/ directory
        Path('file_downloads/').mkdir(exist_ok=True, parents=True)

        # generate PDF
        self.generate_pdf()

        file_name = f'{root_dir}/file_downloads/{self.username}.pdf'
        return file_name

    def return_file_name(self):
        return self.return_pdf_file_path().split('/')[-1]

    def delete_pdf(self):
        """delete pdf file after download"""
        Path(f'{self.return_pdf_file_path()}').unlink(missing_ok=True)


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
