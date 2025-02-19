from django.shortcuts import render

# Create your views here.

# def home(request):
#     return render(request, "home.html")

from django.http import HttpResponse

def home(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to the Home Page</h1>
        <p>This is a simple page rendered directly from the view.</p>
    </body>
    </html>
    """
    return HttpResponse(html_content)
