from odoo import http
from odoo.http import json

class Final_Project(http.Controller):
    @http.route('/finalProject/index' ,auth='public',type="http")
    def index(self, **kw):
        return "Hello world"