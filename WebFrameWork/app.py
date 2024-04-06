from wsgiref.simple_server import make_server


from api import API

app = API()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the Home Page"

@app.route("/")
def template_handler(req,resp):
    resp.body = app.template("index.html",context={"name":"Goutham","title":"Best Framework"}).encode()


@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"

@app.route("/hello/{name}")
def greeting(request,response,name):
    response.text = f"Hello {name}"


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
