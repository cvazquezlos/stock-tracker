from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg2

POSTGRES_DB = 'stock_tracker'
POSTGRES_TABL = 'stocks_historical'
POSTGRES_SCHM = 'public'
POSTGRES_USER = 'postgres'
POSTGRES_PASS = 'Yj18pQ-$20'

class Stock(Resource):
    
    def __init__(self):
        self.status = 0
        try:
            self.conn = psycopg2.connect('dbname=%s user=%s password=%s' % (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASS))
        except:
            self.status = 1
        print(self.conn)
        print("sadsdasdsda")
    
    def get(self, name):
        data = None
        if self.status == 0:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM %s WHERE stock = '%s'" % (POSTGRES_TABL, name))
            data = cur.fetchall()
            cur.close()
            if len(data) > 0:
                return data, 200
            else:
                return "Stock not found", 404
        else:
            return "Internal server error", 500
        
    def get_all(self, name):
        data = None
        if self.status == 0:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM %s" % POSTGRES_TABL)
            data = cur.fetchall()
            cur.close()
            if len(data) > 0:
                return data, 200
            else:
                return "Stocks not found", 404
        else:
            return "Internal server error", 500
        
    def delete(self, name):
        if self.status == 0:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM %s WHERE stock = '%s'" % (POSTGRES_TABL, name))
            deleted_rows = cur.rowcount
            if deleted_rows > 0:
                return "%s is deleted" % name, 200
            else:
                return "Stock not found", 404
            cur.close()
        else:
            return "Internal server error", 500

app = Flask(__name__)
api = Api(app)
api.add_resource(Stock, '/stock/<string:name>')
app.run(debug=True)

