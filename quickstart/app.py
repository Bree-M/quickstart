from flask import Flask, render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///task.db'
db=SQLAlchemy(app)

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    done=db.Column(db.Boolean,default=False)


@app.route('/',methods=['GET','POST']) 
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks=Task.query.all()
        return render_template('index.html',tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()    
    return redirect('/')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Task.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html',task=task)
    
@app.route('/complete/<int:id>')
def complete(id):
    task=Task.query.get_or_404(id)
    task.done=not task.done
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
   app.run()
