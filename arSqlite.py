from sqlite3 import connect

class DbSqlite:
    def __init__(self, local:str=None):
        self.local = local
    
    def connect(self):
        self.conn = connect(self.local)
        return self.conn
    
    def disconnect(self):
        self.conn.close()
    
    def get_tables(self):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM sqlite_master WHERE type='table';""")
        list_to_return = [i[1] for i in cursor.fetchall()]
        self.disconnect()
        return list_to_return
    
    def get_table(self, tabela:str, columns:tuple='*'):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT {str(columns).replace("'", "")} FROM {tabela};""")
        list_to_return = cursor.fetchall()
        self.disconnect()
        return list_to_return
    
    #Retorna lista de colunas de uma tabela.
    def get_table_columns(self, table:str):
        cursor = self.connect().cursor()
        cursor.execute(f"""PRAGMA table_info({table});""")
        lista = cursor.fetchall()
        self.disconnect()
        return [i[1] for i in lista]
    
    #Retorna instância de uma tabela. (key -> [atributo, valor])
    def get_instance(self, table:str, key:list, columns:tuple='*'):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT {columns} FROM {table} WHERE {key[0]} = '{key[1]}'""")
        lista = cursor.fetchall()
        self.disconnect()
        return lista
    
    #Edição de tabelas---------------------------------------------------------
    def new_table(self, name:str, columns:tuple):
        cursor = self.connect().cursor()
        cursor.execute(f"""
        CREATE TABLE {name} {str(columns).replace("'", "")};""")
        self.disconnect()
    
    def new_table_column(self, table_name:str, column_name:str, index:int=-1, standard_value=''):
        columns = self.get_table_columns(table_name)
        if (index > len(columns)) or (-index > len(columns) + 1):
            return print(f'Index "{index}" not accepted') 
        if column_name in columns:
            return print(f'The "{column_name}" column already exists.')
        if index == -1: columns.append(column_name)
        else:
            if index < -1: columns.insert(index+1, column_name)
            else: columns.insert(index, column_name)
        if type(standard_value) == type([]) and (not len(standard_value) == len(self.get_table(table_name))):
            return print(f'The list of values ​​is not properly sized({len(self.get_table(table_name))})!')
        #Salvar table antes e column antes
        table_before = self.get_table(table_name)
        #Excluir table
        self.del_table(table_name)
        #Criar nova tabela
        self.new_table(table_name, tuple(columns))
        #Adicionar valores a nova tabela
        for i in range(len(table_before)):
            x = list(table_before[i])
            if type(standard_value) == type([]): val = standard_value[i]
            else: val = standard_value
            val = str(val)
            if index == -1: x.append(val)
            else:
                if index < -1: x.insert(index+1, val)
                else: x.insert(index, val)
            self.new_instance(table_name, x)
    
    #Excluir coluna de uma tabela
    def del_table_column(self, table_name:str, column_name:str):
        cursor = self.connect().cursor()
        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
        self.disconnect()
    
    #Reordenar coluna
    def reorder_column(self, table_name:str, column_name:str, index_after:int):
        columns = self.get_table_columns(table_name)
        columns.remove(column_name)
        if (index_after > len(columns)) or (-index_after > len(columns) + 1):
            return print(f'Index "{index_after}" not accepted') 
        index_before = self.get_table_columns(table_name).index(column_name)
        column_data = [i[index_before] for i in self.get_table(table_name)]
        #Excluir coluna
        self.del_table_column(table_name, column_name)
        #Criar a coluna novamente
        self.new_table_column(table_name, column_name, index_after, standard_value=column_data)
    
    #Editar colunas de uma tabela
    def edit_table_columns(self, name:str, columns:tuple):
        table_actual_columns = self.get_table_columns(name)
        add_columns = []
        del_columns = []
        for i in table_actual_columns:
            if not i in columns: del_columns.append(i)
        for i in columns:
            if not i in table_actual_columns: add_columns.append(i)
        for i in add_columns: self.new_table_column(name, i)
        for i in del_columns: self.del_table_column(name, i)

    #Exclui uma tabela
    def del_table(self, name:str):
        cursor = self.connect().cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {name}")
        self.disconnect()
    #--------------------------------------------------------------------------
    
    #Cria nova instância de uma tabela. 
    def new_instance(self, table:str, tupla:tuple):
        conn = self.connect()
        cursor = conn.cursor()
        mapa = self.get_table_columns(table)
        cursor.execute(f"""
        INSERT INTO {table} {tuple(i.replace("'", "") for i in mapa)} VALUES {tuple(tupla)}
        """)
        conn.commit()
        self.disconnect()
    
    #Edita instância de uma tabela. (key -> [atributo, valor])
    def edit_instance(self, table:str, key:list, attribute:str, value):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE {table} SET {attribute} = '{value}' WHERE {key[0]} = '{key[1]}'""", ())
        conn.commit()
    
    #Remove instância de uma tabela. (key -> [atributo, valor])
    def del_instance(self, table:str, key:list):
        conn = self.connect()
        cursor = conn.cursor()
        key =  f"WHERE {key[0]} = '{key[1]}'"
        cursor.execute(f"""DELETE FROM {table} {key}""",)
        conn.commit()

def main():
    db = DbSqlite('db.db')
    table_name = 'dados_individuo'

    db.reorder_column(table_name, 'nome', 1)

    print(db.get_table_columns(table_name))
    for i in db.get_table(table_name):
        print(i)
    
if __name__ == '__main__':
    main()
