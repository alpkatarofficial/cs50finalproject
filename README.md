# YOUR CAR FINDER
#### Video Demo:  <https://youtu.be/d9xQgRVgRPU>
#### Description:

  Tthe mental thinking behind this web app is to make a project that really solves "something" in real life as this is one of the things that is sought by the employers. Getting used to utilize generative AI to almost do everything at my job and normal life(pun intended), I also found this idea of establishing a 2nd hand car database app through AI when i asked to it to generate ideas for me that is going to showcase my data analyst skills as someones first portfolio project.

  'Your Car Finder', a Flask based web app, is a used car finder and its analytics tool built together actually. The catch is that the dataset I used for my database is an actual Craiglist dataset with over 420,000 rows of data in it. I have to admit, I had never worked with so much data before. The actual dataset was 1.45 GB big but I cleaned up it in the excel manually by removing the mostly null valued rows, decreasing the column size from 26 to 17. The link to original dataset can be found here: https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data/data

  I can talk about this for too long as i spent many hours for it but I will try to be as concise as possible not to bore you here. Here is what every piece of my apps code does:

app.py: As always it is the heart of the whole app which has multiple routes for multiple pages. In some routes, you can see it combines SQL into Python code so that it can retrieve data from specific columns. This is firstly done as I need to include filtering options for various features of used vehicles so I needed a selector, a crucial step to obtain the relevant data to be used by data analysis tools and graphs.

car.db: The database containing our dataset in a table called "cars_new"(which was written like that as i need to change the table name somewhere along the way)

templates/index.html: The main page of the app, which includes dropdown menus for user to select specific features of the cars such as state, region, manufacturer, vehicle type, vehicle production year, vehicle condition, fuel type, transmission type, vehicle color. I used DISTINCT clauses here in the app.py Python code to retrieve distinct names of the car features here such as: states = query_database("SELECT DISTINCT state FROM cars_new"). As a result of this, I couldn't include the 'Model' dropdown as it was taking too much time to load all of the car models, probably something related the database having over 400k row. After the handles, there are two buttons. 'Find My Car' takes you to the result page. The 'Interactive Visualizations' button is the one taking you to choose visualization type of your liking.

templates/results.html: This is a normal result page, which list the retrieved results from the users query. With JS, I also added the functionality of sorting numeric columns in price, year, and odometer here to make it more realistic. The rows are also clickacle.

templates/car_detail.html: This page works like a template here. When a result(row) is clicked, this page is opened based on the features of the car which changes row to row. I try to imitate a Turkish 2nd hand marketplace site's design here. The next step here might be retrieving the kind of general product images based on the model name from Google images but this would take too much time and wouldn't be very accurate I assume.

templates/visualization_selection.html: A transition page to direct user to the available types of visualizations there are: A scatterplot or pie charts.

templates/scatterplot.html: Scatter plot is a graph that uses dots to represent values for two different numeric variables. Having three numverical variables columns in my dataset, namely price, odometer(mileage), and year(vehicle production year), I used them to be placed in X or Y axises, based on the user preference. Along with that, I also used dropdown filters  such as state, region, manufacturer vehicle type, and production year to have a determine the sample size here. Too much dots(data) was creating problems in the loading time so I also added the dropdown option to have the "LIMIT"ing ability which is going to work like the 'LIMT' clause in SQL query.

templates/scatterresults:  This is where the user's scatter plot is displayed. I used Plotly here to for the scatter plot. When reload the page, it loads the same query with different results as I determined that having random would serve a better purpose. As for data analyst portfolio addition, adding written SQL query based on user searches was the last addition to this page, with and extra addition to the copy the sql query.

templates/pie_chart.html: A transition page enabling user to choose one of the 4 available types of pie chart options: Vehicle Condition, Vehicle Status, Manufacturer Share, Fuel Type

templates/pie_condition.html: This page allows you to generate a pie chart displaying the vehicle conditions such as "like new" and "good" in number and percentages given the selected state and/or vehicle type from the dropdown menus.

templates/pie_title_status.html: This page allows you to generate a pie chart displaying the vehicle statuses such as "clean" and "salvage" in number and percentages given the selected state dropdown menu.

templates/pie_manufacturer.html: This page allows you to generate a pie chart displaying the vehicle manufacturers such as "honda" and "bmw" in number and percentages given the selected state or states altogether if multiple states selected.

templates/pie_fuel.html: This page allows you to generate a pie chart displaying the vehicles' fuel types such as "gas" and "electric" in number and percentages given the selected state or states and/or selected region or regions. The thing is that if selected regions are not in the selected state or states, the chart shows nothing. So this chart should be used with some precise geography knowledge but can be very helpful in comparing the market trend/consumer preferences between the whole states and their counties.

styles.css: Some CSS to make sure taht everything is displayed in a great way. For display, I just used bootstrap and in HTML CSSs so there is not much else in the seperate CSS file.

PS: For this app, I used ChatGPT very much as otherwise it would have taken me so long to write all the HTMLs and the logic of addin SQL queries to the app.py. However, it was different this time. Usually, just copy pasting codes from GPT to my work at my job, this time I copy pasted code snippets and added little bits and bits myself also tweaking the actual structure. Thank you for this course. 










