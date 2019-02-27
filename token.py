# This file is part of Coog. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import os
import binascii

from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval

__all__ = [
    'Token',
    ]


class Token(ModelSQL, ModelView):
    'API Token'
    __name__ = 'api.token'

    active = fields.Boolean('Active')
    name = fields.Char('Name', required=True)
    key = fields.Char('Key', states={'invisible': ~Eval('key')})
    user = fields.Many2One('res.user', 'User', required=True)
    party = fields.Many2One('party.party', 'Party')

    @classmethod
    def default_active(cls):
        return True

    @classmethod
    def check(cls, key):
        tokens = cls.search([('key', '=', key)])
        if tokens:
            token = tokens[0]
            return token.user.id, token.party.id if token.party else None
        else:
            return None, None

    @classmethod
    def create(cls, vlist):
        for values in vlist:
            if not values.get('key'):
                values['key'] = binascii.hexlify(
                    os.urandom(24)).decode('ascii')
        return super(Token, cls).create(vlist)
