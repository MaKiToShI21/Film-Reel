from django.http import HttpResponse


def homepage(request):
    return HttpResponse(f"""<h1>Добро пожаловать в FilmReel!</h1>""")

def about(request):
    return HttpResponse("<h1>О проекте FilmReel</h1><p>Это учебный проект по Django</p>")

def contact(request):
    return HttpResponse("""
        <h1>Контакты</h1>
        <p>Email: info@filmreel.com</p>
        <p>Телефон: +7 (123) 456-78-90</p>
    """)
