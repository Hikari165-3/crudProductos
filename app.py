from flask import Flask, request, render_template,redirect,url_for,session

app=Flask(__name__)
app.secret_key='unaclavesecreta'

#funcion
def generar_id():                   #sesion el objeto productos
    if 'productos' in session and len(session['productos'])>0:
        #el id de registro mayor y le sumamos +1
        return max(item['id'] for item in session['productos'])+1
    else:
        return 1


@app.route("/")
def index():
    if 'productos' not in session:
        session['productos']=[]
    productos=session.get('productos',[])
    return render_template('index.html',productos=productos)


@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method=='POST':
        nombre=request.form['nombre']
        cantidad=request.form['cantidad']
        precio=request.form['precio']
        fecha_vencimiento=request.form['fecha_vencimiento']
        categoria=request.form['categoria']
        nuevo_producto={
            'id':generar_id(),
            'nombre':nombre,
            'cantidad':cantidad,
            'precio':precio,
            'fecha_vencimiento':fecha_vencimiento,
            'categoria':categoria
        }
        if 'productos' not in session:
            #en caso de que no exista lista de productos en la sesion
            session['productos']=[]#objeto lista sesion 
            
        session['productos'].append(nuevo_producto)
        session.modified=True
        return redirect(url_for('index'))
    return render_template("nuevo.html")
                #parametro
@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_productos=session.get('productos',[])
    #realiza un recorrido a los productos y si no lo encuentra no muestra na, next extrae
    registro=next((c for c in lista_productos if c['id']==id),None)
    if not registro:
        return redirect(url_for('index'))
    if request.method=='POST':
        registro['nombre']=request.form['nombre']
        registro['cantidad']=request.form['cantidad']
        registro['precio']=request.form['precio']
        registro['fecha_vencimiento']=request.form['fecha_vencimiento']
        registro['categoria']=request.form['categoria']
        session.modified=True
        return redirect(url_for('index'))
    return render_template('editar.html',registro=registro)#le manda un diccionario al html

@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    lista_productos=session.get('productos',[])
                #sacar lo elementos de la lista de productos 
    registro=next((c for c in lista_productos if c['id']==id),None)
    if registro:
        #remover esa informacion de la sesion
        session['productos'].remove(registro)
        session.modified=True
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True,port='5017')








