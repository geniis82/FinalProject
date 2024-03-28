import jwt
from odoo import http
from odoo.http import request


class AuthenticationController(http.Controller):

    @http.route('/auth/login', type='json', auth='public', methods=['POST'])
    def login(self, **kwargs):
        data = request.httprequest.json
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
            if user:
                authenticated_user = user.authenticate("odoodb", username, password, request.httprequest.environ)
                if authenticated_user:
                    # Generar un token de acceso JWT
                    payload = {'user_id': user.id}
                    token = jwt.encode(payload, 'secret', algorithm='HS256')
                    return {"status": 201, 'accessToken': token}
                # else:
                #     return {"status": 400, 'error': 'Credenciales inválidas'}
            else:
                return {"status": 400, 'error': 'Usuario no encontrado'}
        else:
            return {"status": 400, 'error': 'Se requieren nombre de usuario y contraseña'}


