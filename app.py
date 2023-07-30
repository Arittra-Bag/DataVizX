from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No File Selected!')

        if file:
            try:
                # Read the CSV file into a Pandas DataFrame
                df = pd.read_csv(file)

                # Get the selected visualization type from the form
                visualization_type = request.form['visualization_type']

                # Filter out non-numeric columns for correlation matrix calculation
                numeric_columns = df.select_dtypes(include=[float, int]).columns
                df_numeric = df[numeric_columns]

                # Create the selected visualization based on user input
                if visualization_type == 'bar':
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title='Bar Chart')
                    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
                elif visualization_type == 'pie':
                    fig = px.pie(df, values=df[df.columns[1]], names=df[df.columns[0]], title='Pie Chart')
                elif visualization_type == 'scatter':
                    fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title='Scatter Plot')
                    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
                elif visualization_type == 'line':
                    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Line Graph')
                    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
                elif visualization_type == 'correlation':
                    # Create a correlation matrix using Plotly
                    correlation_matrix = df_numeric.corr()
                    fig = go.Figure(data=go.Heatmap(z=correlation_matrix.values, x=correlation_matrix.columns, y=correlation_matrix.columns))

                # Convert the Plotly figure to HTML and store it in the 'visualization' variable
                visualization_html = fig.to_html(full_html=False)

                return render_template('result.html', visualization=visualization_html)

            except pd.errors.ParserError:
                return render_template('index.html', error='Invalid CSV file format!')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
