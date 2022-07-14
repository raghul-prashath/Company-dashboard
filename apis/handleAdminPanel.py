from . import * 

#Admin Panel
def addView():
    admin.add_view(UsersController(Users, db.session))
    admin.add_view(CoreController(Core, db.session))
    admin.add_view(spController(SpecialRights, db.session))
    admin.add_link(MenuLink(name='Logout',url="/logout"))
