
from flask import  render_template, jsonify, request, url_for, redirect, session, g
from application import app
app.secret_key='jajalolXD'

class persona:
    def __init__(self,number,usrnm,pw):
       self.id = number
       self.name = usrnm
       self.code = pw
    def __repr__(self):
        return f'<User: {self.name}>'

class campo:
    def __init__(self,tittle,desc):
        self.titulo = tittle
        self.trabajos = desc

class tarea:
    def __init__(self,tittle,desc):
        self.tittle = tittle
        self.descripcion = desc

numero = 1
usuarios = []
fields = []

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    global numero
    global usuarios
    if(request.method=='POST'):
        usuarios.append(persona(numero,request.form['username'], request.form['password'])) 
        numero += 1
        return redirect(url_for('login'),code = 307) 
    return render_template('signin.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None;
    global usuarios
    if len(usuarios) != 0:
        if request.method == 'POST': 
            session.pop('user_id',None)
            nombre = request.form['username']
            clv = request.form['password']
            user = None
            for x in usuarios:
                if x.name == nombre:
                    user = x
                    break
            if user and user.code == clv:
                session['user_id'] = user.id
                return redirect(url_for('home')) 
            else:
                error="error al ingresar usuario y/o password. Intenta de nuevo."
    else:
        error = "no existen usuarios todavia. Se el primero :D y haz click en sign in"
    return render_template('login.html',error=error)

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('work'))
    return render_template('home.html', user = [x for x in usuarios if x.id == session['user_id']][0])

@app.route('/work',methods = ['GET','POST'])
def work():
    global fields
    if request.method == 'POST':
        cosa = request.form['objeto']
        if cosa == 'CAMPO':
            creo = request.form['crear']
            if creo == 'CREATE':
                name = request.form['tittle']
                aux = []
                fields.append(campo(name,aux))
            elif creo == 'DELETE':
                name = request.form['tittle']
                i = 0
                for x in fields:
                    if name == x.titulo:
                        fields.pop(i)
                    i += 1
        if cosa == 'TAREA':
            accion = request.form['crear']
            if accion == 'CREATE' and len(fields) >= 1:
                ttl = request.form['tittle']
                desc = request.form['descripcion']
                place = request.form['lugar']
                for x in fields:
                    if place == x.titulo:
                        x.trabajos.append(tarea(ttl,desc))
            elif accion == 'DELETE' and len(fields) >= 1:
                buscar = request.form['tittle']
                place = request.form['lugar']
                i = 0
                for x in fields:
                    if place == x.titulo:
                        j = 0
                        for y in x.trabajos:
                            if buscar == y.tittle:
                                x.trabajos.pop(j)
                        j+=1
                    i += 1
        print(len(fields[0].trabajos))
    return render_template('work_desk.html', campos = fields,)