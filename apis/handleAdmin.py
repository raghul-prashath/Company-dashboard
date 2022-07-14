from . import *

class Controllers(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('adminLogin'))


class UsersController(Controllers):
    column_list = ('adminId', 'empId', 'name')
    def is_accessible(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[6]):
                return True
        return False
        
    @property
    def can_create(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[2]):
                return True
        return False

    @property
    def can_read(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[3]):
                return True
        return False

    @property
    def can_edit(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[4]):
                return True
        return False

    @property
    def can_delete(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[5]):
                return True
        return False

class CoreController(Controllers):
    def is_accessible(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[7]):
                return True
        return False
        
    @property
    def can_create(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[2]):
                return True
        return False

    @property
    def can_read(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[3]):
                return True
        return False
        
    @property
    def can_edit(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[4]):
                return True
        return False

    @property
    def can_delete(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[5]):
                return True
        return False


class spController(Controllers):
    column_list = ('role','adminId','create','read','update','delete','usersTable','coreTable')
    def is_accessible(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[8]):
                return True
        return False
        
    @property
    def can_create(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[2]):
                return True
        return False

    @property
    def can_read(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[3]):
                return True
        return False
        
    @property
    def can_edit(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[4]):
                return True
        return False

    @property
    def can_delete(self):
        records=getSpecialRights(current_user.empId)
        for record in records:
            if bool(record[5]):
                return True
        return False


@event.listens_for(Users.password,'set',retval=True)
def hashPass(target,value,oldvalue,initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value).decode('utf-8')
    return value
    
@login_manager.user_loader
def load_user(id):
    return Users.query.filter_by(empId=id).first()

@app.route('/admin/login',methods=['POST','GET'])
def adminLogin():    
    if request.method== 'POST':
        empId = request.form.get('empId')
        password = request.form.get('password')
        records = selectEmp(empId)
        user = Users.query.filter_by(name=empId).first()
        
        if records == None:
            flash('Invalid credentials')
            return render_template('login.html', head='Admin Panel')

        elif bcrypt.check_password_hash(records[3], password):
            if records[0]!=2:
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('admin.index'))
            else:
                flash('Invalid credentials')
                return render_template('login.html', head='Admin Panel')

        else:   
            flash('Invalid credentials')
            return render_template('login.html', head='Admin Panel')
    else:  
        return render_template('login.html', head='Admin Panel')


@app.route('/dash', methods=['POST','GET'])
@login_required
def dash():
    cust = ''
    if request.method == 'POST':
        try:
            df = pd.read_csv(request.files.get('file'))
            db.engine.execute("delete from core;")
            for i in range(len(df)):
                db.session.add(Core(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3], df.iloc[i, 4], df.iloc[i, 5], df.iloc[i, 6], df.iloc[i, 7], df.iloc[i, 8], df.iloc[i, 9]))
            db.session.commit()
            
        except:
            cust = request.form['Filter']
        
        
    customers_obj = db.engine.execute("select distinct(customerName) from core;")
    customer = [i[0] for i in customers_obj]
    if(len(customer)==0):
        return render_template('graph.html', head='Dashboard', customer='', data=[], cust='', database = 0, flag = 0)
    if(len(cust)==0):
        cust = customer[0]

    customer.append("All_customers")
    flag = 0
    if(cust != "All_customers"):
        UATplan = db.engine.execute("select UAT, planUATDate, count(planUATDate) from core where customerName='"+ cust +"' group by planUATDate ORDER BY planUATDate ASC;")
        UATact = db.engine.execute("select UAT, actUATDate, count(actUATDate) from core where customerName='"+ cust +"' group by actUATDate ORDER BY actUATDate ASC;")
        PRODplan = db.engine.execute("select PROD, planProdDate, count(planProdDate) from core where customerName='"+ cust +"' group by planProdDate ORDER BY planProdDate ASC;")
        PRODact = db.engine.execute("select PROD, actProdDate, count(actProdDate) from core where customerName='"+ cust +"' group by actProdDate ORDER BY actProdDate ASC;")
    else:
        flag = 1
        UATplan = db.engine.execute("select  UAT, planUATDate, count(planUATDate), customerName from core group by planUATDate,customerName ORDER BY planUATDate ASC;")
        UATact = db.engine.execute("select UAT, actUATDate, count(actUATDate), customerName from core group by actUATDate,customerName ORDER BY actUATDate ASC;")
        PRODplan = db.engine.execute("select PROD, planProdDate, count(planProdDate), customerName from core group by planProdDate,customerName ORDER BY planProdDate ASC;")
        PRODact = db.engine.execute("select PROD, actProdDate, count(actProdDate), customerName from core group by actProdDate,customerName ORDER BY actProdDate ASC;")


    tot = db.engine.execute("select count(*) from core where customerName='"+ cust +"';")
    total_count = [i[0] for i in tot][0]

    UATplanlist = [list(i) for i in UATplan]
    PRODplanlist = [list(i) for i in PRODplan]
    UATactlist = [list(i) for i in UATact]
    PRODactlist = [list(i) for i in PRODact]

    if flag==0:
        for lists in UATplanlist:
            a = db.engine.execute("select issueKey from core where customerName='" + cust + "' and planUATDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in UATactlist:
            a = db.engine.execute("select issueKey from core where customerName='" + cust + "' and actUATDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in PRODplanlist:
            a = db.engine.execute("select issueKey from core where customerName='" + cust + "' and planProdDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in PRODactlist:
            a = db.engine.execute("select issueKey from core where customerName='" + cust + "' and actProdDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
    else:
        for lists in UATplanlist:
            a = db.engine.execute("select issueKey from core where customerName='" + lists[-1] + "' and planUATDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in UATactlist:
            a = db.engine.execute("select issueKey from core where customerName='" + lists[-1] + "' and actUATDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in PRODplanlist:
            a = db.engine.execute("select issueKey from core where customerName='" + lists[-1] + "' and planProdDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
        
        for lists in PRODactlist:
            a = db.engine.execute("select issueKey from core where customerName='" + lists[-1] + "' and actProdDate='" + lists[1] + "'" )
            lista= ", ".join([i[0] for i in a])
            lists.append(lista)
    

    data = [UATplanlist, UATactlist, PRODplanlist, PRODactlist]
    dataname = ["UAT Planned Data", "UAT Actual Data", "PROD Planned Data", "PROD Actual Data"]
    
    for planlist in data:
        j=-1
        count = 0

        for i in range(len(planlist)):
            if planlist[i][0] == None:
                planlist[i][0] = "Unnamed"
            if planlist[i][1] == None:
                planlist[i][1] = "Unassigned Date"
            if planlist[i][2] == 0:
                j=i
            else:
                count+=planlist[i][2]

        if(j!=-1):
            planlist[j][2] = total_count-count


    return render_template('graph.html', head=cust +' Dashboard', customer=sorted(customer), data=data, cust=cust, database = 1, flag = flag, dataname = dataname)

@app.route('/',methods=['POST','GET'])
def userLogin():    
    if request.method== 'POST':
        empId = request.form.get('empId')
        password = request.form.get('password')
        records = selectEmp(empId)
        user = Users.query.filter_by(name=empId).first()
        
        if records == None:
            flash('Invalid credentials')
            return render_template('login.html', head='User Panel')

        elif bcrypt.check_password_hash(records[3], password):
            if records[0]==1 or records[0]==2:
                login_user(user)
                return redirect(url_for('dash'))
            else:
                flash('Invalid credentials')
                return render_template('login.html', head='User Panel')

        else:   
            flash('Invalid credentials')
            return render_template('login.html', head='User Panel')
    else:  
        return render_template('login.html', head='User Panel')

@app.route('/logout')
@login_required
def adminLogout():    
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('adminLogin'))



