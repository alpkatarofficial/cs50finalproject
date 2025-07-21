import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to query the database
def query_database(query, params=()):
    connection = sqlite3.connect('car.db')
    cursor = connection.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    connection.close()
    return results

# This fetches the car by ID and passes it to the car_detail.html template.
@app.route('/car/<int:car_id>')
def car_detail(car_id):
    query = "SELECT * FROM cars_new WHERE id = ?"
    car = query_database(query, (car_id,))

    image_query = "SELECT image_url FROM model_images WHERE model = ?"  # hypothetical table
    car_image = query_database(image_query, (car[0][5],)) if car else None
    car_image_url = car_image[0][0] if car_image else None

    if car:
        return render_template('car_detail.html', car=car[0], car_image_url=car_image_url)
    else:
        return "<h3>Car not found.</h3>", 404



# Home route - Displays the form to filter cars
@app.route('/')
def index():
    # Fetch the unique values for dropdowns (as follows id, region, manufacturer, model, year, price, condition, odometer)
    ids = query_database("SELECT DISTINCT id FROM cars_new")
    states = query_database("SELECT DISTINCT state FROM cars_new")
    regions = query_database("SELECT DISTINCT region FROM cars_new")
    manufacturers = query_database("SELECT DISTINCT manufacturer FROM cars_new")
    types = query_database("SELECT DISTINCT type FROM cars_new")
    models = query_database("SELECT DISTINCT model FROM cars_new")
    years = query_database("SELECT DISTINCT year FROM cars_new")
    prices = query_database("SELECT DISTINCT price FROM cars_new")
    conditions = query_database("SELECT DISTINCT condition FROM cars_new")
    odometers = query_database("SELECT DISTINCT odometer FROM cars_new")
    fuels = query_database("SELECT DISTINCT fuel FROM cars_new")
    transmissions = query_database("SELECT DISTINCT transmission FROM cars_new")
    colors = query_database("SELECT DISTINCT paint_color FROM cars_new")

    return render_template('index.html', ids=ids, states=states, regions=regions, manufacturers=manufacturers, types=types, models=models, years=years, prices=prices, conditions=conditions, odometers=odometers, fuels=fuels, tranmissions=transmissions, colors=colors)


@app.route('/visualizationselections')
def visualization_selections():
    return render_template('visualization_selections.html')

# PIE CHART ROUTES
@app.route('/piechart')
def piechart():
    return render_template('pie_chart.html')

#1 PIE CHART CONDITION ROUTE
@app.route('/piechart/condition', methods=['GET', 'POST'])
def piechart_condition():
    states = query_database("SELECT DISTINCT state FROM cars_new")
    types = query_database("SELECT DISTINCT type FROM cars_new")

    chart_data = []
    sql_query = ""

    if request.method == 'POST':
        selected_state = request.form.get('state')
        selected_type = request.form.get('type')

        query = "SELECT condition, COUNT(*) FROM cars_new WHERE 1=1"
        params = []

        if selected_state:
            query += " AND LOWER(TRIM(state)) = LOWER(TRIM(?))"
            params.append(selected_state)

        if selected_type:
            query += " AND LOWER(TRIM(type)) = LOWER(TRIM(?))"
            params.append(selected_type)

        query += " GROUP BY condition"
        sql_query = query
        chart_data = query_database(query, params)

    return render_template("pie_condition.html", states=states, types=types,
                           chart_data=chart_data, sql_query=sql_query)



#2 PIE CHART STATUS ROUTE
@app.route('/piechart/title_status', methods=['GET', 'POST'])
def piechart_title_status():
    chart_data = None
    sql_query = ""

    connection = sqlite3.connect('car.db')
    cursor = connection.cursor()

    # Fetch dropdown values
    cursor.execute("SELECT DISTINCT state FROM cars_new ORDER BY state")
    states = cursor.fetchall()

    if request.method == 'POST':
        state = request.form.get('state')

        query = "SELECT title_status, COUNT(*) FROM cars_new WHERE 1=1"
        params = []

        if state:
            query += " AND LOWER(TRIM(state)) = LOWER(TRIM(?))"
            params.append(state)

        query += " GROUP BY title_status"
        sql_query = query.replace("?", "'{}'").format(*params)  # for display

        cursor.execute(query, params)
        chart_data = cursor.fetchall()

    connection.close()

    return render_template("pie_title_status.html", chart_data=chart_data, sql_query=sql_query, states=states)


#3 PIE CHART MANU ROUTE
@app.route('/piechart/manufacturer', methods=['GET', 'POST'])
def piechart_manufacturer():
    chart_data = None
    sql_query = ""

    connection = sqlite3.connect('car.db')
    cursor = connection.cursor()

    # Get all distinct states for multi-select dropdown
    cursor.execute("SELECT DISTINCT state FROM cars_new ORDER BY state")
    states = cursor.fetchall()

    if request.method == 'POST':
        selected_states = request.form.getlist('states')

        query = "SELECT manufacturer, COUNT(*) FROM cars_new WHERE 1=1"
        params = []

        if selected_states:
            placeholders = ",".join("?" for _ in selected_states)
            query += f" AND LOWER(TRIM(state)) IN ({placeholders})"
            params.extend([state.lower().strip() for state in selected_states])

        query += " GROUP BY manufacturer"
        sql_query = query.replace("?", "'{}'").format(*params)

        cursor.execute(query, params)
        chart_data = cursor.fetchall()

    connection.close()

    return render_template("pie_manufacturer.html", chart_data=chart_data, sql_query=sql_query, states=states)


#4 PIE CHART FUEL ROUTE
@app.route('/piechart/fuel', methods=['GET', 'POST'])
def piechart_fuel():
    connection = sqlite3.connect('car.db')
    cursor = connection.cursor()

    # Fetch dropdown values
    cursor.execute("SELECT DISTINCT state FROM cars_new")
    states = cursor.fetchall()
    cursor.execute("SELECT DISTINCT region FROM cars_new")
    regions = cursor.fetchall()

    chart_data = []
    sql_query = ""

    if request.method == 'POST':
        selected_states = request.form.getlist('states')
        selected_regions = request.form.getlist('regions')

        query = "SELECT fuel, COUNT(*) FROM cars_new WHERE 1=1"
        conditions = []
        params = []

        if selected_states:
            placeholders = ','.join(['?'] * len(selected_states))
            conditions.append(f"state IN ({placeholders})")
            params.extend(selected_states)

        if selected_regions:
            placeholders = ','.join(['?'] * len(selected_regions))
            conditions.append(f"region IN ({placeholders})")
            params.extend(selected_regions)

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY fuel"
        sql_query = query.replace('?', '{}').format(*[f"'{p}'" for p in params])

        cursor.execute(query, params)
        chart_data = cursor.fetchall()

    connection.close()
    return render_template('pie_fuel.html', states=states, regions=regions, chart_data=chart_data, sql_query=sql_query)




# SCATTER PLOT ROUTE
@app.route('/scatterplot', methods=['GET'])
def scatterplot():
    # Fetch values for dropdowns
    states = query_database("SELECT DISTINCT state FROM cars_new")
    regions = query_database("SELECT DISTINCT region FROM cars_new")
    manufacturers = query_database("SELECT DISTINCT manufacturer FROM cars_new")
    types = query_database("SELECT DISTINCT type FROM cars_new")
    years = query_database("SELECT DISTINCT year FROM cars_new")

    # Define valid numeric fields
    numeric_fields = ['price', 'odometer', 'year']

    return render_template('scatterplot.html',states=states, regions=regions, manufacturers=manufacturers, types=types, years=years, numeric_fields=numeric_fields)

# SCATTERPLOT VISUALIZATION RESULTS
@app.route('/scatterplot/scatterresults', methods=['POST'])
def scatterplot_results():
    state = request.form.get('state')
    region = request.form.get('region')
    manufacturer = request.form.get('manufacturer')
    type = request.form.get('type')
    year = request.form.get('year')
    x_axis = request.form.get('x_axis')
    y_axis = request.form.get('y_axis')
    sample_size = int(request.form.get('sample_size', 1000))

    valid_numeric_fields = ['price', 'odometer', 'year']
    if x_axis not in valid_numeric_fields or y_axis not in valid_numeric_fields:
        return "Invalid axis selection", 400

    base_query = "SELECT price, odometer, year FROM cars_new WHERE 1=1"
    params = []

    if state:
        base_query += " AND state = ?"
        params.append(state)
    if region:
        base_query += " AND region = ?"
        params.append(region)
    if manufacturer:
        base_query += " AND manufacturer = ?"
        params.append(manufacturer)
    if type:
        base_query += " AND type = ?"
        params.append(type)
    if year:
        base_query += " AND year = ?"
        params.append(year)

    rows = query_database(base_query, params)

    import random
    if len(rows) > sample_size:
        rows = random.sample(rows, sample_size)

    full_data = [dict(zip(['price', 'odometer', 'year',], row)) for row in rows]

    # Reconstruct SQL query string with values for display
    sql_query = base_query
    for val in params:
        replacement = f"'{val}'" if isinstance(val, str) else str(val)
        sql_query = sql_query.replace('?', replacement, 1)
    sql_query += f" LIMIT {sample_size}"


    return render_template(
        'scatterresults.html',
        full_data=full_data,
        fields=valid_numeric_fields,
        x_axis=x_axis,
        y_axis=y_axis,
        sql_query=sql_query
    )






# Filter route - Displays the filtered results
@app.route('/results', methods=['POST'])
def results():
    id = request.form.get('id')
    state = request.form.get('state')
    region = request.form.get('region')
    manufacturer = request.form.get('manufacturer')
    type = request.form.get('type')
    model = request.form.get('model')
    year = request.form.get('year')
    price = request.form.get('price')
    condition = request.form.get('condition')
    odometer = request.form.get('odometer')
    fuel = request.form.get('fuel')
    transmission = request.form.get('transmission')
    color = request.form.get('paint_color')



    # Filter the cars based on the selected criteria
    query = "SELECT * FROM cars_new WHERE 1=1"
    params = []

    if id:
        query += " AND id = ?"
        params.append(id)

    if state:
        query += " AND LOWER(TRIM(state)) = LOWER(TRIM(?))"
        params.append(state)

    if region:
        query += " AND LOWER(TRIM(region)) = LOWER(TRIM(?))"
        params.append(region)

    if manufacturer:
        query += " AND manufacturer = ?"
        params.append(manufacturer)

    if type:
        query += " AND LOWER(TRIM(type)) = LOWER(TRIM(?))"
        params.append(type)

    if model:
        query += " AND LOWER(TRIM(model)) = LOWER(TRIM(?))"
        params.append(model)

    if year:
        query += " AND year = ?"
        params.append(year)

    if price:
        query += " AND price = ?"
        params.append(price)

    if condition:
        query += " AND LOWER(TRIM(condition)) = LOWER(TRIM(?))"
        params.append(condition)

    if odometer:
        query += " AND odometer = ?"
        params.append(odometer)

    if fuel:
        query += " AND LOWER(TRIM(fuel)) = LOWER(TRIM(?))"
        params.append(fuel)

    if transmission:
        query += " AND LOWER(TRIM(transmission)) = LOWER(TRIM(?))"
        params.append(transmission)

    if color:
        query += " AND LOWER(TRIM(paint_color)) = LOWER(TRIM(?))"
        params.append(color)


    #cars = query_database(query, params)
    #return render_template('results.html', cars=cars)

    readable_query = query
    for p in params:
        if isinstance(p, str):
            p = f"'{p}'"
        readable_query = readable_query.replace("?", str(p), 1)

    cars = query_database(query, params)
    return render_template('results.html', cars=cars, sql_query=readable_query)

if __name__ == '__main__':
    app.run(debug=True)

