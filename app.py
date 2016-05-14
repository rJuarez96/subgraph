import os
from flask import *
import subgraphIsomorphism

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        clauses = request.form.get('clauses',False,type=str)
        clauses2 = request.form.get('clauses2',False,type=str)
        clausesCon=clauses+"/"+clauses2
        clausesCon2=clauses+"------------------------"+clauses2

        if(not clauses):
            return render_template('index.html',clausula = clausesCon2,maxclique="Escriba una clausula")
        maxclique = subgraphIsomorphism.create(str(clausesCon))
        return render_template('index.html',clausula = clausesCon2,maxclique = maxclique )
    else:
        return render_template('index.html',maxclique="Escriba una clausula")
	
if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8081)),debug=True)
