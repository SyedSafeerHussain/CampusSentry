from flask import Flask,render_template
import pandas as pd
app=Flask(__name__)

@app.route('/')
def dashboard():
    try:
        df=pd.read_csv("std.csv")
        table_html=df.to_html(classes='table table-striped',index=False)
        return render_template('dashboard.html',table=table_html)
    except Exception as e:
        return f"<h3>Error loading data: {e}</h3>"
if __name__=="__main__":
    app.run(debug=True)
