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
        <a href="https://nitrobills-backend-backup.onrender.com/api/docs/">Go to the Api Docs</a>
        </br>
        <a href="https://nitrobills-backend-backup.onrender.com/api/schema">Download Api Schema</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)
