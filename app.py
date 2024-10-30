from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://Spider:vortex@localhost/blog_db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=dt.now)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_contemt = request.form['content']
        new_task = Todo(content=task_contemt)

        try:
            
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except Exception as e:
            raise e
            return 'There was an issue'
        # end try
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("home.html", tasks=tasks)
    

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/')
    except Exception as e:
        raise e
        return 'There was a problem deleting the task'
    # end try


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
      task.content = request.form['content']

      try:
        # comment: 
        db.session.commit()

        return redirect('/')
      except Exception as e:
        raise e
        return 'There was a problem updating the task'
      
      # end try
    else:
        return  render_template("update.html", task=task)
   

@app.route("/addTask")
def about():
    return render_template("addTask.html")

if __name__ == "__main__":
    # Ensure the database tables are created before starting the server
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
