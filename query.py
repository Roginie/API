#contex com banco de dados e enviar os dados para o dash
#pip install mysql-connector-python

#conexao
import mysql.connector
import pandas as pd

def conexao(query):
    conn = mysql.connector.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        password= "senai@134",
        db = "bd_carro"
    )

    dataframe = pd.read_sql(query, conn) 
    # EXECUTA A CONSULTA SQL E AMAZENA O RESULTADO EM DATAFRAME

    conn.close()
    return dataframe