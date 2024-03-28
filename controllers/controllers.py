from odoo import http
from odoo.http import json

class Final_Project(http.Controller):
    @http.route(['/finalProject/getUsers','/finalProject/getUsers/<int:userid>'] ,auth='public',type="http")
    def getUsers(self,userid=None,**kw):
        if userid:
            domain=[("id","=",userid)]
        else:
            domain=[]
        userdata= http.request.env["res.users"].sudo().search_read(domain,["name","email"])
        data={"status":200,"data":userdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype="application/json")