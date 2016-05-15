import os
from flask import *
import subgraphIsomorphism

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        clauses = request.form.get('clauses',False,type=str)
        clauses2 = request.form.get('clauses2',False,type=str)
        clausesCon=str(clauses)+"/"+str(clauses2)
        clausesCon2=str(clauses)+"------------------------"+str(clauses2)
        test=request.form.get('clausesN',False,type=str)
        test2=request.form.get('clausesN2',False,type=str)
        testCon=str(test)+"/"+str(test2)
        testCon2=str(test)+"------------------------"+str(test2)


        if(not clauses):
            if(not test):
                return render_template('index.html',clausula = clausesCon2,maxclique="Ingrese un grafo")
            maxclique = subgraphIsomorphism.create(str(testCon))  
            return render_template('index.html',clausula = str(testCon2),maxclique = maxclique )      
        maxclique = subgraphIsomorphism.create(str(clausesCon))
        
        return render_template('index.html',clausula = str(clausesCon2),maxclique = maxclique )
    else:
        return render_template('index.html',maxclique="Ingrese un grafo")
	
if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8081)),debug=True)
