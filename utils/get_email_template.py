from string import Template


def get_email_template(emailname: str) -> Template:
    print(emailname)
    with open(f'../emails/{emailname}.html', 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
        return Template(template_content)