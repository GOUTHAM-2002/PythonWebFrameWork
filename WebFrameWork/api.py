from webob import Request, Response
from parse import parse
import os
from jinja2 import Environment, FileSystemLoader


class API:
    def __init__(self,templates_dir="templates"):
        self.routes = {}

        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))

    def template(self,template_name,context=None):
        if context is None:
            context={}
        return self.templates_env.get_template(template_name).render(**context)

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Such route already exists")
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)
        return response(environ, start_response)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path,request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found"

    def handle_request(self, request):

        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response
