from sqlite3 import connect

class Db:
    def __init__(self, local:str=None):
        self.local = local
    
    def connect(self):
        self.conn = connect(self.local)
        return self.conn
    
    def disconnect(self):
        self.conn.close()
    
    def get_table(self, tabela:str):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM {tabela};""")
        list_to_return = cursor.fetchall()
        self.disconnect()
        return list_to_return
    
    def get_table_columns(self, table:str):
        cursor = self.connect().cursor()
        cursor.execute(f"""PRAGMA table_info({table});""")
        lista = cursor.fetchall()
        self.disconnect()
        return tuple([i[1] for i in lista])
    
    def get_instance(self, table:str, key:list):
        cursor = self.connect().cursor()
        cursor.execute(f"""SELECT * FROM {table} WHERE {key[0]} = '{key[1]}'""")
        lista = cursor.fetchall()
        self.disconnect()
        return lista
    
    def new_table(self, table_name:str, table_columns:str):
        cursor = self.connect().cursor()
        cursor.execute(f"""
        CREATE TABLE {table_name} {str(table_columns).replace("'", "")};""")
        self.disconnect()
    
    #New, edit e del
    def new_instance(self, table:str, tupla:tuple):
        conn = self.connect()
        cursor = conn.cursor()
        mapa = self.get_table_columns(table)
        cursor.execute(f"""
        INSERT INTO {table} {tuple(i.replace("'", "") for i in mapa)} VALUES {tuple(tupla)}
        """)
        conn.commit()
        self.disconnect()
    
    def edit_instance(self, table:str, key:list, attribute:str, value):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"""
                            UPDATE {table}
                            SET {attribute} = '{value}'
                            WHERE {key[0]} = '{key[1]}'
                            """, ())
        conn.commit()
    
    def del_instance(self, table:str, key:list):
        conn = self.connect()
        cursor = conn.cursor()
        key =  f"WHERE {key[0]} = '{key[1]}'"
        cursor.execute(f"""
                        DELETE FROM {table} {key}
                        """,)
        conn.commit()
        
    
if __name__ == '__main__':
    pass
        