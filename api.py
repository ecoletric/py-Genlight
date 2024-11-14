from flask import Flask as f, request,jsonify
import oracledb

def conexao():
  con = oracledb.connect('rm556448/fiap24@oracle.fiap.com.br:1521/orcl')
  print('Conectado')
  print(con.version)
  return con

app = f(__name__)

@app.route("/empresa/<id:int>", methods=['GET'])
def listarEmpresas(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM EMPRESA WHERE ID_EMPRESA = :id", {"id":id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_empresa':dados[0],
            'nome_empresa':dados[1],
            'cnpj':dados[2],
            'email':dados[3],
            'senha':dados[4],
            'id_endereco':dados[5]
                }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500
    
@app.route('/empresa',methods=['GET'])
def listarTodasEmpresas():
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM EMPRESA")
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                empresa = {
                    'id_empresa':linha[0],
                    'nome_empresa':linha[1],
                    'cnpj':linha[2],
                    'email':linha[3],
                    'senha':linha[4],
                    'id_endereco':linha[5]
                }
                resultado.append(empresa)
                status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500



@app.route('/empresa',methods=['POST'])
def criarEmpresa():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO EMPRESA (nm_empresa, nr_cnpj, email,senha,t_gl_endereco_id_endereco) values (:nome,:cnpj,:email,:senha,:id_endereco)", {'nome':dados['nome'],'cnpj':dados['cnpj'],'email':dados['email'],'senha':dados['senha'],'id_endereco':dados['id_endereco']})
        con.commit()
        cur.execute("SELECT * FROM t_gl_empresa WHERE ROWNUM = 1 ORDER BY id_empresa DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_empresa':dados[0],
            'nome_empresa':dados[1],
            'cnpj':dados[2],
            'email':dados[3],
            'senha':dados[4],
            'id_endereco':dados[5]
                }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/empresa/<int:id>',methods=['PUT'])
def atualizarEmpresa(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE EMPRESA SET  email = :email, senha = :senha WHERE id_empresa = :id", {'email':dados['email'],'senha':dados['senha'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM EMPRESA WHERE id_empresa = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
                'id_empresa':dados[0],
                'nome_empresa':dados[1],
                'cnpj':dados[2],
                'email':dados[3],
                'senha':dados[4],
                'id_endereco':dados[5]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/empresa/<int:id>',methods=['DELETE'])
def excluirEmpresa(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM EMPRESA WHERE id_empresa = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Empresa excluída com sucesso"}), 200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/endereco/<id:int>", methods=['GET'])
def listarEndereco(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM ENDERECO WHERE ID_ENDERECO = :id", {"id":id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_endereco':dados[0],
            'cep':dados[1],
            'logradouro':dados[2],
            'complemento':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/endereco',methods=['POST'])
def criarEndereco():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO ENDERECO (cep, logradouro, complemento) values (:cep,:logradouro,:complemento)", {'cep':dados['cep'],'logradouro':dados['logradouro'],'complemento':dados['complemento']})
        con.commit()
        cur.execute("SELECT * FROM ENDERECO WHERE ROWNUM = 1 ORDER BY id_endereco DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_endereco':dados[0],
            'cep':dados[1],
            'logradouro':dados[2],
            'complemento':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/endereco/<int:id>',methods=['PUT'])
def atualizarEndereco(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE ENDERECO SET cep = :cep, logradouro = :logradouro, complemento = :complemento WHERE id_endereco = :id", {'cep':dados['cep'],'logradouro':dados['logradouro'],'complemento':dados['complemento'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM ENDERECO WHERE id_endereco = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_endereco':dados[0],
            'cep':dados[1],
            'logradouro':dados[2],
            'complemento':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/endereco/<int:id>',methods=['DELETE'])
def excluirEndereco(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM ENDERECO WHERE id_endereco = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Endereço excluído com sucesso"}), 200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500


@app.route('/maquina',methods=['POST'])
def inserirMaquina():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO t_gl_maquina (consumo,ds_maquina,t_gl_sitio_id_sitio) values (:consumo,:ds_maquina,:id_sitio)", {'consumo':dados['consumo'],'ds_maquina':dados['ds_maquina'],'id_sitio':dados['id_sitio']})
        con.commit()
        cur.execute("SELECT * FROM t_gl_maquina WHERE ROWNUM = 1 ORDER BY id_maquina DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_maquina':dados[0],
            'consumo':dados[1],
            'ds_maquina':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)

@app.route('/maquina/<int:id>',methods=['PUT'])
def atualizarMaquina(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE t_gl_maquina SET consumo = :consumo, ds_maquina = :ds_maquina, t_gl_sitio_id_sitio = :id_sitio WHERE id_maquina = :id", {'consumo':dados['consumo'],'ds_maquina':dados['ds_maquina'],'id_sitio':dados['id_sitio'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM t_gl_maquina WHERE id_maquina = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_maquina':dados[0],
            'consumo':dados[1],
            'ds_maquina':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/maquina/<int:id>',methods=['DELETE'])
def excluirMaquina(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM t_gl_maquina WHERE id_maquina = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Maquina excluída com sucesso"}),200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/maquina/<id:int>", methods=['GET'])
def listarMaquina(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_maquina WHERE id_maquina = :id", {"id":id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_maquina':dados[0],
            'consumo':dados[1],
            'ds_maquina':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/maquina/listar/<id:ind>", methods=['GET'])
def listarMaquinas(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_maquina where id_sitio = :id", {"id":id})
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                maquina = {
                'id_maquina':linha[0],
                'consumo':linha[1],
                'ds_maquina':linha[2],
                'id_sitio':linha[3]
                }
                resultado.append(maquina)
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado),status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500


@app.route("/aparelhoGerado", methods=['POST'])
def inserirAparelhoGerado():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO (potencia,tipo,t_gl_sitio_id_sitio) values (:potencia,:tipo,:id_sitio)", {'potencia':dados['potencia'],'tipo':dados['tipo'],'id_sitio':dados['id_sitio']})
        con.commit()
        cur.execute("SELECT * FROM t_gl_aparelho_gerado WHERE ROWNUM = 1 ORDER BY id_aparelho_gerado DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_aparelho_gerado':dados[0],
            'potencia':dados[1],
            'tipo':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/aparelhoGerado/<int:id>',methods=['PUT'])
def atualizarAparelhoGerado(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE t_gl_aparelho_gerado SET potencia = :potencia WHERE id_aparelho_gerado = :id", {'potencia':dados['potencia'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM t_gl_aparelho_gerado WHERE id_aparelho_gerado = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_aparelho_gerado':dados[0],
            'potencia':dados[1],
            'tipo':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/aparelhoGerado/<int:id>',methods=['DELETE'])
def excluirAparelhoGerado(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM t_gl_aparelho_gerado WHERE id_aparelho_gerado = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Aparelho Gerado excluído com sucesso"}), 200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/aparelhoGerado/<id:int>", methods=['GET'])
def listarAparelhoGerado(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_aparelho_gerado WHERE id_aparelho_gerado = :id", {"id":id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_aparelho_gerado':dados[0],
            'potencia':dados[1],
            'tipo':dados[2],
            'id_sitio':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/aparelhoGerado/listar/<id:ind>", methods=['GET'])
def listarAparelhosGerados(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_aparelho_gerado where id_sitio = :id", {"id":id})
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                aparelho = {
                'id_aparelho_gerado': linha[0],
                'potencia': linha[1],
                'tipo': linha[2],
                'id_sitio': linha[3]
                }
                resultado.append(aparelho)
                status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/sitio", methods=['POST'])
def inserirSitio():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO t_gl_sitio (tp_fonte,t_gl_industria_id_industria,t_gl_endereco_id_endereco) values (:tp_fonte,:id_industria,:id_endereco)", {'tp_fonte':dados['tp_fonte'],'id_industria':dados['id_industria'],'id_endereco':dados['id_endereco']})
        con.commit()
        cur.execute("SELECT * FROM t_gl_sitio WHERE ROWNUM = 1 ORDER BY id_sitio DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_sitio':dados[0],
            'tp_fonte':dados[1],
            'id_industria':dados[2],
            'id_endereco':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/sitio/<int:id>',methods=['PUT'])
def atualizarSitio(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE t_gl_sitio SET tp_fonte = :tp_fonte WHERE id_sitio = :id", {'tp_fonte':dados['tp_fonte'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM t_gl_sitio WHERE id_sitio = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_sitio':dados[0],
            'tp_fonte':dados[1],
            'id_industria':dados[2],
            'id_endereco':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/sitio/<int:id>',methods=['DELETE'])
def excluirSitio(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM t_gl_sitio WHERE id_sitio = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Sitio excluído com sucesso"}),200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route("/sitio/<id:int>", methods=['GET'])
def listarSitio(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_sitio WHERE id_sitio = :id", {"id":id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_sitio':dados[0],
            'tp_fonte':dados[1],
            'id_industria':dados[2],
            'id_endereco':dados[3]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500
    
@app.route("/sitio/listar/<id:ind>", methods=['GET'])
def listarSitios(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_sitio where id_industria = :id", {"id":id})
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                sitio = {
                'id_sitio':linha[0],
                'tp_fonte':linha[1],
                'id_industria':linha[2],
                'id_endereco':linha[3]
                }
                resultado.append(sitio)
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500



@app.route("/industria", methods=['POST'])
def inserirIndustria():
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("INSERT INTO t_gl_industria (nm_industria,t_gl_empresa_id_empresa) values (:nm_industria,:id_empresa)", {'nm_industria':dados['nm_industria'],'id_empresa':dados['id_empresa']})
        con.commit()
        cur.execute("SELECT * FROM t_gl_industria WHERE ROWNUM = 1 ORDER BY id_industria DESC")
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_industria':dados[0],
            'nm_industria':dados[1],
            'id_empresa':dados[2]
            }
            status = 200
        else:
            resultado = {}
            status = 404 
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/industria/<int:id>',methods=['PUT'])
def atualizarIndustria(id):
    try:
        con = conexao()
        cur = con.cursor()
        dados = request.json()
        cur.execute("UPDATE t_gl_industria SET nm_industria = :nm_industria WHERE id_industria = :id", {'nm_industria':dados['nm_industria'],'id':id})
        con.commit()
        cur.execute("SELECT * FROM t_gl_industria WHERE id_industria = :id", {'id':id})
        dados = cur.fetchone()
        if dados:
            resultado = {
            'id_industria':dados[0],
            'nm_industria':dados[1],
            'id_empresa':dados[2]
            }
            status = 200
        else:
            resultado = {}
            status = 404
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

@app.route('/industria/<int:id>',methods=['DELETE'])
def excluirIndustria(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("DELETE FROM t_gl_industria WHERE id_industria = :id", {'id':id})
        con.commit()
        cur.close()
        con.close()
        return jsonify({"mensagem": "Industria excluída com sucesso"}),200
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}),500

@app.route("/industria/<id:int>", methods=['GET'])
def listarIndustria(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_industria WHERE id_industria = :id", {"id":id})
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                industria = {
                'id_industria':linha[0],
                'nm_industria':linha[1],
                'id_empresa':linha[2]
                }
                resultado.append(industria)
            status = 200
        else:
            resultado = {}
            status = 404
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500

            
@app.route('/industria/listar/<id:int>',methods=['GET'])
def listarTodasIndustrias(id):
    try:
        con = conexao()
        cur = con.cursor()
        cur.execute("SELECT * FROM t_gl_industria where id_empresa = :id", {"id":id})
        dados = cur.fetchall()
        if dados:
            resultado = []
            for linha in dados:
                industria = {
                'id_industria':linha[0],
                'nm_industria':linha[1],
                'id_empresa':linha[2]
                }
                resultado.append(industria)
            status = 200
        else:
            resultado = {}
            status = 404
        cur.close()
        con.close()
        return jsonify(resultado), status
    except oracledb.DatabaseError as db_err:
        print("Erro de banco de dados: ", db_err)
        return jsonify({"erro": "Erro de banco de dados"}), 500