from . import *


class SpecialRights(db.Model):
    __tablename__="specialRights"
    
    adminId= db.Column('adminId', db.Integer,primary_key=True)
    role=db.Column('role', db.String(30), unique=True, nullable=False)
    create = db.Column('create',db.Boolean)
    read = db.Column('read',db.Boolean)
    update = db.Column('update',db.Boolean)
    delete = db.Column('delete',db.Boolean)
    usersTable=db.Column('usersTable',db.Boolean)
    coreTable=db.Column('coreTable',db.Boolean)
    spTable=db.Column('spTable',db.Boolean)

    def __init__(self,adminId,role,create,read,update,delete,usersTable,coreTable,spTable):
        self.adminId=adminId
        self.role = role
        self.create = create
        self.read = read
        self.update = update
        self.delete = delete
        self.usersTable=usersTable
        self.coreTable=coreTable
        self.spTable=spTable


    
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    empId = db.Column('empId',db.Integer, primary_key=True)
    adminId = db.Column('adminId',db.Integer, db.ForeignKey('specialRights.adminId'))
    roles = db.relationship("SpecialRights", backref='adminId_SpecialRights')
    name = db.Column('name', db.String(30))
    password = db.Column('password', db.String(300))
    
    def __init__(self, empId, name, password, adminId):
        self.empId = empId
        self.adminId = adminId
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def get_id(self):
        return (self.adminId)


class Core(db.Model):
    __tablename__ = 'core'
    coreId = db.Column('core Id', db.Integer, primary_key=True)
    customerName = db.Column('customerName', db.String(30))
    issueKey = db.Column('issueKey', db.String(30))
    issueType = db.Column('issueType', db.String(30))
    status = db.Column('status', db.String(30))
    UAT = db.Column('UAT', db.String(30))
    PROD = db.Column('PROD', db.String(30))
    planUATDate = db.Column('planUATDate', db.String(30))
    planProdDate = db.Column('planProdDate', db.String(30))
    actUATDate = db.Column('actUATDate', db.String(30))
    actProdDate = db.Column('actProdDate', db.String(30))

    def __init__(self, customerName, issueType, issueKey, UAT, PROD, planUATDate, planProdDate, actUATDate, actProdDate,  status):
        self.customerName = customerName
        self.issueKey = issueKey
        self.issueType = issueType
        self.UAT = UAT
        self.PROD = PROD
        self.status = status
        self.planUATDate = planUATDate
        self.planProdDate = planProdDate
        self.actUATDate = actUATDate
        self.actProdDate = actProdDate
        
    def get_id(self):
        return (self.courseId)
        
# handleDb to Handle initial Db operations
def handleDb():
    db.create_all()    
    if not SpecialRights.query.all():
        db.session.add(SpecialRights(1,'admin',True,True,True,True,True,True,True))
        db.session.add(SpecialRights(2,'user',False,False,False,False,False,False,False))
        db.session.commit()
    if not Users.query.all():
        db.session.add(Users('1','user','user',2))
        db.session.commit()
        db.session.add(Users('0','core','core',1))
        db.session.commit()
    


def getSpecialRights(adminId):
    rights=SpecialRights.query.filter_by(adminId=adminId)    
    records=[]
    for rows in rights:
        records.append((rows.adminId, rows.role, rows.create, rows.read, rows.update, rows.delete, rows.usersTable, rows.coreTable, rows.spTable))
    return records 


#Register user    
def registerUser(empId, name, password, roles):
    exist=SpecialRights.query.filter_by(role=roles).first()    
    if exist:
        db.session.add(Users(empId, name, password, exist.adminId))
        db.session.commit()
    
#Select email to check if there is no matching email   
def selectEmp(empId):
    user=Users.query.filter_by(name=empId).first()
    if user:
        return [user.adminId,user.empId,user.name,user.password]
    else:
        return None

#check user Id
def checkEmpId(empId):
    EmpId=Users.query.filter_by(empId=empId).first()
    if EmpId:
        return 1
    else:
        return 0
