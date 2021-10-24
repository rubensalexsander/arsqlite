from sqlite3 import connect

class Db:
    def __init__(self, local=None):
        self.local = local
    
    def connect(self):
        self.conn = connect(self.local)
        return self.conn
    
    def disconnect(self):
        self.conn.close()
    
    def getTabela(self, tabela):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM {tabela};""")
        list_to_return = cursor.fetchall()
        self.disconnect()
        return list_to_return
    
    def getInstancia(self, tabela, key):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM {tabela} WHERE {key[0]} = '{key[1]}'""")
        lista = cursor.fetchall()
        self.disconnect()
        return lista
    
    def novaTabela(self, nomeTabela, atributosTabela):
        
        cursor = self.connect().cursor()

        cursor.execute(f"""
        CREATE TABLE {nomeTabela} {str(atributosTabela).replace("'", "")};
        """)

        self.disconnect()
    
    #Adicionar, editar e deletar
    def novaInstancia(self, tabela, mapa, tupla):
        conn = self.connect()
        cursor = conn.cursor()
        # inserindo dados na tabela
        cursor.execute(f"""
        INSERT INTO {tabela} {tuple(i.replace("'", "") for i in mapa)} VALUES {tuple(tupla)}
        """)
        conn.commit()
        self.disconnect()
        return f'{tabela} adicionada com sucesso!'
    
    def editarInstancia(self, tabela, id, atributo, valor):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"""
                            UPDATE {tabela}
                            SET {atributo} = '{valor}'
                            WHERE id = '{id}'
                            """, ())
        conn.commit()
        return "Dados atualizados com sucesso."
    
    def delInstancia(self, tabela, key):
        conn = self.connect()
        cursor = conn.cursor()
        key =  f"WHERE {key[0]} = '{key[1]}'"
        cursor.execute(f"""
                        DELETE FROM {tabela} {key}
                        """,)
        conn.commit()
        return "Dados deletados com sucesso."
        
    
if __name__ == '__main__':
    db1 = Db('C:\Arquivos\Arquivos Sincronizados\Meus arquivos\z_Outros\ESTUDOS\Programação\PROJETOS\Python\Cont\CONT\cont V2.0\db\db.db')
    print(db1.getInstancia('sociode', ['id', '#17132']))
        