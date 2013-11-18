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

    def __init__(self, genre, code, msg, http_code=None):
        self.genre = genre
        self.code = code
        self.msg = msg
        self.http_code = http_code

    def __str__(self):
        if http_code is not None:
            return "JsonException(type={%s}, code={%d}, msg={%d}, http_code={%d})" % (self.genre, self.code, self.msg, self.http_code)
        else:
            return "JsonException(type={%s}, code={%d}, msg={%d})" % (self.genre, self.code, self.msg)
            
            
class PayutcJsonClient(object):

    def __init__(self, url, service, user_agent="python jsonclient", cookie=None):
        u"""Crée un client lié à un service

        Arguments :
        url -- url de base du serveur
        service -- le service avec lequel le client est lié
        user_agent -- le user agent qu'utilisera le client
        cookie -- un cookie à transmettre au serveur
        
        Lève une JsonClientError si le serveur ne renvoie pas un code 200
        
        """
        
        self.url = "%s/%s/" % (url, service)
        self.user_agent = user_agent
        self.cookie = cookie
        

    def api_call(self, func, params=None):
        u"""Se connecte au service pour chercher le résultat de func(params)
        Retourne la réponse sous la forme d'un objet python (list, dict, boolean, …) 

        Arguments :
        func -- méthode du service à appeler
        params -- dict des arguments de la fonction
        
        Lève une PayutcJsonClientError si le serveur ne renvoie pas un code 200
        
        """
        
        headers = {'User-Agent': self.user_agent}

        url = "%s%s" % (self._url, func)
        
        if self._cookie is not None:
            headers['Cookie'] = self.cookie
            
        r = requests.post(url, data=params)
            
        if r.status_code is not requests.codes.ok:
            raise PayutcJsonClientError("InvalidHTTPCode", 37, "La page n'a pas renvoyé un code 200.", r.status_code)

        self._cookie = r.cookies
            
        return r.json()

    def __getattr__(self, func, **params):
        u"""Modification de __getattr__ permettant l'appel de fonctions du service
        sous la forme :
            >>>client.loginApp(key=XXX)
            True

        Arguments :
        func -- méthode du service à appeler
        **params -- arguments de la fonction
        
        
        """
        return self.api_call(func, params)

    
    
        



