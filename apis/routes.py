from . import *  

def routesApi():
    api.add_resource(register,'/users/register')
    api.add_resource(login,'/users/login')
    api.add_resource(refresh,'/refresh')
    api.add_resource(tokenData,'/data')
    api.add_resource(logout,'/users/logout')
    
