from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']  = 'postgres://gyouvwfwrulzoc:e5d5aac9c8d12829e4cf040647c47c4d591ebc5e7a21a74621c2118723dda3c6@ec2-3-89-214-80.compute-1.amazonaws.com:5432/d1nl7s88j145vb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class Notas(db.Model):
    '''Clase notas'''
    __tablename__ = "notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(300))

    def __init__(self, tituloNota, cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        print(nota.tituloNota)
        print(nota.cuerpoNota)
    return render_template("leernotas.html", consulta = consulta_notas)

@app.route('/crearnota', methods=['POST'])
def crearnota():
    campoTitulo = request.form["campoTitulo"]
    campoCuerpo = request.form["campoCuerpo"]
    if campoCuerpo == "" or campoCuerpo == "":
        return render_template("index.html", respuesta = "¡Verifica que hayas colocado los datos correctamente!")
    else:
        notaNueva = Notas(tituloNota = campoTitulo,cuerpoNota = campoCuerpo)
        db.session.add(notaNueva)
        db.session.commit()
        return render_template("index.html", cuerpo = campoCuerpo, titulo = campoTitulo)


@app.route("/eliminarnota/<ID>")
def eliminar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).delete()
    print (nota)
    db.session.commit()
    return redirect("/leernotas")

@app.route("/modificar", methods=["POST"])
def modificarnota():
    idnota = request.form['idNota']
    ntitulo = request.form['campoTitulo']
    ncuerpo = request.form['campoCuerpo']
    nota = Notas.query.filter_by(idNota = int(idnota)).first()
    nota.tituloNota = ntitulo
    nota.cuerpoNota = ncuerpo
    db.session.commit()
    return redirect("/leernotas")

@app.route("/editarnota/<ID>")
def editar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).first()
    print (nota)
    print (nota.tituloNota)
    print (nota.cuerpoNota)
    return render_template("modificar.html", nota = nota)



if __name__ == "__main__":
    db.create_all()
    app.run()