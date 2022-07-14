from . import *

class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False
    def is_accessible(self):
        return current_user.is_authenticated