"""
Napisz aplikację we flasku, posiadającą jeden endpoint /customers
Po wejściu na niego metodą GET powinno wypisać wszystkich customerów wraz z przy
pisanymi do nich adresami w formie tabelki albo listy punktowej (znaczniki <ul></ul>)
Pod tabelką, albo listą customerów powinien znaleźć się formularz służący do uzu
pełnienia adresu dla podanego customera, format powinien być taki:
- id użytkownika, dla którego wpisujemy adres
- nazwa miasta
- nazwa ulicy
- numer domu
Po zaakceptowaniu formularza powinno wysłać się żądanie POST na ten sam endpoint
 z odpowiednimi danymi.
"""

from flask import Flask, request, render_template
from psycopg2 import connect

app = Flask(__name__)
con = connect(user = 'postgres', password = 'coderslab', host = 'localhost', dbname = 'exercises_db')
cur = con.cursor()

@app.route('/')
def form():
    html = """
    <h3>Podstrona /customers wyświetla i modyfikuje dane adresowe klientów</h3>
    <ul>
      <li><a href='/customers'>Customers</li>     
    </ul>
    """
    return html

@app.route('/customers', methods = ['GET', 'POST'])
def db_data_actions():
    sql_view = """select * 
                from customers 
                left join addresses on (customers.customer_id = addresses.customer_id);"""

    if request.method == 'GET':
        cur.execute(sql_view)
        db_data = cur.fetchall()
        return render_template('index.html', db_data = db_data)  #szukaj w katalogu /templates , db_data=db_data,
    else:
        if request.form['action'] == 'Dodaj':
            sql_mod = f"""insert into addresses(customer_id, city, street, house_number)
                        values({request.form.get('customer_id')}, 
                                '{request.form.get('city')}',
                                '{request.form.get('street')}', 
                                {request.form.get('house_number')});"""
        elif request.form['action'] == 'Zmień':
            sql_mod = f"""update addresses 
                            set city = '{request.form.get('city')}', 
                                street = '{request.form.get('street')}', 
                                house_number = {request.form.get('house_number')} 
                            where customer_id = {request.form.get('customer_id')};"""
        elif request.form['action'] == 'Usuń':
            sql_mod = f"""delete from addresses where customer_id = {request.form.get('customer_id')};"""
        else:
            sql_mod = ''

        cur.execute(sql_mod)
        con.commit()
        cur.execute(sql_view)
        db_data = cur.fetchall()
        return render_template('index.html', db_data = db_data)


if __name__ == '__main__':
    app.run('localhost', 5000)