import sqlite3
import logging

#------------------
db_logger = logging.getLogger(__name__)
db_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/db_control.log')
formatter = logging.Formatter('%(name)s :: %(asctime)s :: %(levelname)s :: %(message)s')
file_handler.setFormatter(formatter)
db_logger.addHandler(file_handler)
#------------

def adduser(id : str, db_name : str, table_name : str):
    db_logger.info('Attempting to add user {} into the {} database into the {} table'.format(id, db_name, table_name))
    try:
        sqlite_connection = sqlite3.connect(db_name)
        db_logger.info("Successfuly connected to the database")
        cursor = sqlite_connection.cursor()
        db_logger.info("Successfully added cursor")
        insert_comm = '''INSERT OR IGNORE INTO {}
                        VALUES ({});
                        '''.format(table_name, id)
        cursor.execute(insert_comm)
        sqlite_connection.commit()
        db_logger.info("Successfully commited the changes to the table")
        cursor.close()
    except:
        db_logger.exception("A problem has occured while trying to add user {} into the {} database into the {} table".format(id, db_name, table_name))

def removeuser(id : str, db_name : str, table_name : str):
    db_logger.info('Attempting to remove user {} from the {} database from the {} table'.format(id, db_name, table_name))
    try:
        sqlite_connection = sqlite3.connect(db_name)
        db_logger.info("Successfuly connected to the database")
        cursor = sqlite_connection.cursor()
        db_logger.info("Successfully added cursor")
        remove_comm = '''DELETE FROM {}
                        WHERE id = {};
                        '''.format(table_name, id)
        cursor.execute(remove_comm)
        sqlite_connection.commit()
        db_logger.info("Successfully commited the changes to the table")
        cursor.close()
    except:
        db_logger.exception("A problem has occured while trying to remove user {} from the {} database from the {} table".format(id, db_name, table_name))
    
def getusers(db_name : str, table_name : str):
    db_logger.info("Attempting to extract users from the {} database from the {} table".format(db_name, table_name))
    try:
        sqlite_connection = sqlite3.connect(db_name)
        db_logger.info("Successfuly connected to the database")
        cursor = sqlite_connection.cursor()
        db_logger.info("Successfully added cursor")
        insert_comm = "SELECT * FROM {}".format(table_name)
        cursor.execute(insert_comm)
        res = cursor.fetchall()
        sqlite_connection.commit()
        db_logger.info("Successfully commited the changes to the table")
        cursor.close()
        return res
    except:
        db_logger.exception("A problem has occured while trying to extract users from the {} database from the {} table".format(id, db_name, table_name))
        return []
    
def FindProducts(comp_name : str, db_name : str, table_name : str):
    try:
        sqlite_connection = sqlite3.connect(db_name)
        db_logger.info("Successfuly connected to the database")
        cursor = sqlite_connection.cursor()
        db_logger.info("Successfully added cursor")
        insert_comm = '''SELECT *
                        FROM {}
                        WHERE formatted_name = '{}';
                        '''.format(table_name, comp_name)
        cursor.execute(insert_comm)
        output = cursor.fetchall()
        cursor.close()
        return output
    except:
        db_logger.exception("A problem has occured while trying to extract info about company {} from the {} database from the {} table".format(comp_name, db_name, table_name))

def FindCompanies(prod_name : str, db_name : str, table_name : str):
    try:
        sqlite_connection = sqlite3.connect(db_name)
        db_logger.info("Successfuly connected to the database")
        cursor = sqlite_connection.cursor()
        db_logger.info("Successfully added cursor")
        insert_comm = '''SELECT full_name
                        FROM {}
                        WHERE {} = 1;
                        '''.format(table_name, prod_name)
        cursor.execute(insert_comm)
        output = cursor.fetchall()
        cursor.close()
        return output
    except:
        db_logger.exception("A problem has occured while trying to extract info about {} product from the {} database from the {} table".format(prod_name, db_name, table_name))