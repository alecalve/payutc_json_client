#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  payutc_json_client
#  
#  Copyright 2013 Antoine LE CALVEZ <antoine@alc.io>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import requests



class PayutcJsonClientError(Exception):

    def __init__(self, genre, msg, http_code=None):
        self.genre = genre
        self.msg = msg
        self.http_code = http_code

    def __str__(self):
        if http_code is not None:
            return "JsonException(type={%s}, msg={%d}, http_code={%d})" % (self.genre, self.code, self.http_code)
        else:
            return "JsonException(type={%s}, msg={%d})" % (self.genre, self.msg)
            
            
class PayutcJsonClient(object):

    def __init__(self, url, service, user_agent="python jsonclient"):
        u"""Crée un client lié à un service

        Arguments :
        url -- url de base du serveur
        service -- le service avec lequel le client est lié
        user_agent -- le user agent qu'utilisera le client
        
        Lève une JsonClientError si le serveur ne renvoie pas un code 200
        
        """
        
        self.url = url
        self.user_agent = user_agent
        self.service = service
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        
    def set_service(self, service):
        self.service = service

    def get_cookie(self):
        return self.session.cookies["PHPSESSID"]

    def set_cookie(self, cookie):
        self.session.cookies["PHPSESSID"] = cookie

    def call(self, func, **params):
        u"""Se connecte au service pour chercher le résultat de func(params)
        Retourne la réponse sous la forme d'un objet python (list, dict, boolean, …) 

        Arguments :
        func -- méthode du service à appeler
        params -- dict des arguments de la fonction
        
        Lève une PayutcJsonClientError si le serveur ne renvoie pas un code 200
        
        """

        if not func:
            raise ValueError("Le paramètre func doit être fourni")
            
        url = "%s/%s/%s" % (self.url, self.service, func)

        r = self.session.post(url, data=params)
            
        if r.status_code is not requests.codes.ok:
            raise PayutcJsonClientError("InvalidHTTPCode", "La page n'a pas renvoyé un code 200.", r.status_code)
            
        return r.json()

if __name__ == '__main__':
    c = PayutcJsonClient("http://payutc.code.localhost/server/web", "POSS3")

    
    
        



