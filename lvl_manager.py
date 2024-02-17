import sqlite3
from shutil import copy as shutil_copy
from pygame._sdl2 import messagebox

class Lvl_manager:
    def __init__(self, DB_path) -> None:
        self.path = DB_path
        self.DB: sqlite3.Connection = sqlite3.connect(self.path)
        self.cursor: sqlite3.Cursor = self.DB.cursor()

        # Leer base de datos
        self.base_de_datos = sqlite3.connect(self.path)
        self.cursor = self.base_de_datos.cursor()
        try:
            self.cursor.execute("SELECT * FROM Niveles")
        except:
            self.base_de_datos.close()
            shutil_copy('./lvls.sqlite3',self.path)
            self.base_de_datos = sqlite3.connect(self.path)
            self.cursor = self.base_de_datos.cursor()
            self.cursor.execute("SELECT * FROM Niveles")

        

    def search_lvl_blocks(self, id:int = None) -> list[tuple]:
        self.cursor.execute("SELECT b.*, c.* FROM Bloques b INNER JOIN Colores c ON c.id = b.id_color WHERE id_lvl=?",[id])
        datos = self.cursor.fetchall()
        return datos
    
    def search_custom_lvl_blocks(self, id:int = None) -> list[tuple]:
        self.cursor.execute("SELECT b.*, c.* FROM Bloques_2 b INNER JOIN Colores c ON c.id = b.id_color WHERE id_lvl=?",[id])
        datos = self.cursor.fetchall()
        return datos
    
    def search_web_lvl_blocks(self, id:int = None) -> list[tuple]:
        self.cursor.execute("SELECT b.*, c.* FROM Bloques_online b INNER JOIN Colores c ON c.id = b.id_color WHERE id_lvl=?",[id])
        datos = self.cursor.fetchall()
        return datos
    
    def search_custom_lvls_list(self) -> list[tuple[int|str]]:
        self.cursor.execute("SELECT * FROM Niveles_2")
        datos = self.cursor.fetchall()
        return datos

    def match_color(self,color: tuple[int,int,int], n=0) -> int:
        if n > 3: return 1
        r,g,b = color
        self.cursor.execute("SELECT * FROM Colores WHERE red=? AND green=? AND blue=?",[r,g,b])
        if result := self.cursor.fetchall():
            return result[0][0]
        self.cursor.execute("INSERT INTO Colores VALUES(NULL,?,?,?)",[r,g,b])
        self.base_de_datos.commit()
        return self.match_color(color,n+1)
    
    def guardar_nivel(self,name,bloques:list) -> None:
        try:
            self.cursor.execute('INSERT INTO Niveles_2 Values(NULL,?)',[name])
            self.cursor.execute('SELECT * FROM Niveles_2 WHERE nombre=?',[name])
            lvl_id = self.cursor.fetchone()[0]
            for a in bloques:
                datos = [
                    lvl_id,
                    self.match_color(a['color']),
                    a['rect'].x,
                    a['rect'].y,
                    a['rect'].width,
                    a['rect'].height,
                    a['effect'],
                    a['border_radius'],
                    a.get('power',0)
                ]
                self.cursor.execute("INSERT INTO Bloques_2 VALUES(?,?,?,?,?,?,?,?,?)",datos)
            self.base_de_datos.commit()
        except sqlite3.IntegrityError:
            messagebox(
                "Error",
                f"El nombre del perfil ya fue escogido",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=0,
            )
    
    def guardar_nivel_online(self,data: dict) -> bool:
        try:
            self.cursor.execute('INSERT INTO Niveles_online Values(?,?)',[data['id'],data['nombre']])
            
            for a in data['bloques']:
                datos = [
                    data['id'],
                    self.match_color(a['color']),
                    a['x'],
                    a['y'],
                    a['width'],
                    a['height'],
                    a['effect'],
                    a['border_radius'],
                    a.get('power',0)
                ]
                self.cursor.execute("INSERT INTO Bloques_online VALUES(?,?,?,?,?,?,?,?,?)",datos)
            self.base_de_datos.commit()
        except sqlite3.IntegrityError:
            return True
        return False

    def check_online_lvl(self, id: int) -> bool:
        self.cursor.execute('SELECT * FROM Niveles_online WHERE id=?',[id])
        return (len(self.cursor.fetchall()) > 0)

    def delete_custom_lvl(self, id) -> None:
        if id == '' or id == None or id == False:
            return False

        try:
            self.cursor.execute("DELETE FROM Niveles_2 WHERE id=?",[id])
        except Exception as e:
            messagebox(
                "Error",
                f"A ocurrido un error al eliminar el nivel\n{e}",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=1,
            )
        try:
            self.cursor.execute("DELETE FROM Bloques_2 WHERE id_lvl=?",[id])
        except Exception as e:
            messagebox(
                "Error",
                f"A ocurrido un error al eliminar los bloques del nivel\n{e}",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=1,
            )
        self.base_de_datos.commit()