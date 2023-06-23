from flask import Flask, render_template, request, redirect, session
from app import app
from models import *
from datetime import datetime
from matplotlib import pyplot as plt


app.secret_key = "Something"

@app.route("/", methods=['GET', 'POST'])
def u_login():
    if request.method == 'GET':
        return render_template('root.html')
    elif request.method == 'POST':
        d = dict()
        for p in Users.query.all():
            d[p.username] = p.password
        if request.form['username'] in d.keys():
            if d[request.form['username']] == request.form['password']:
                session['username'] = request.form['username']
                return redirect(f"/{request.form['username']}/dashboard")
            else:
                return redirect("/")
        else:
            person = Users(username = request.form['username'], password = request.form['password'])
            db.session.add(person)
            db.session.commit()
            session['username'] = request.form['username']
            return redirect(f"/{request.form['username']}/dashboard")
    



@app.route("/<username>/dashboard") 
def clientDashboard(username):
  client = Users.query.filter_by(username = username).first()
  all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
  shadow = ShadowManager.query.filter_by(user_id=client.user_id).first()
  if shadow:
    logs=Logs.query.filter_by(shadow_id=shadow.shadow_id).all()
    if logs:
      last_log=logs[-1]
      return render_template('client_dashboard.html', user = client, trackers=all_shadows, last=last_log)
      
    else:
      return render_template('new_client_dashboard.html', user = client, trackers=all_shadows)
    
  else:
    return render_template('new_client_dashboard.html', user = client, trackers=all_shadows)
    
    



@app.route("/add_new_shadow/<username>", methods = ["GET", "POST"])
def addShadow(username):
  if request.method == 'GET':
    client = Users.query.filter_by(username = username).first()
    all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
    return render_template('shadowManagement.html', user=client, trackers=all_shadows)
  
  if request.method == 'POST':
    client = Users.query.filter_by(username = username).first()
    
    shadow_name = request.form['Tracker_name']
    about = request.form['Description']
    shadow_type = request.form['Tracker_type']
    inputs = ShadowManager(shadow_name=shadow_name, about=about, shadow_type=shadow_type,user_id=client.user_id,last_seen = datetime.now())
    db.session.add(inputs)
    db.session.commit()
    return redirect(f'/{username}/dashboard')




@app.route("/add_new_log/<username>/<shadow_id>", methods = ["GET", "POST"])
def logs1(username, shadow_id):
  if request.method == 'GET':
    client = Users.query.filter_by(username = username).first()
    all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    all_logs = Logs.query.filter_by(user_id=client.user_id).all()
    
    return render_template(f'{shadow.shadow_type}.html', user=client, all_logs=all_logs, all_trackers=all_shadows, tracker=shadow)
  
    
  
  if request.method == 'POST':
    client = Users.query.filter_by(username = username).first()
    all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    
    value = request.form['value']
    note = request.form['note']
    inputs = Logs(time =  datetime.now(), value=value, note=note,user_id=client.user_id, shadow_id=shadow.shadow_id)
    db.session.add(inputs)
    db.session.commit()
    return redirect(f'/{username}/{shadow_id}')



@app.route("/<username>/<shadow_id>")
def client_shadow(username, shadow_id):
  client = Users.query.filter_by(username = username).first()
  all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
  shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()

  all_logs = Logs.query.filter_by(shadow_id=shadow_id).all()
  
  return render_template('shadow.html', user = client, all_trackers=all_shadows, all_logs=all_logs,tracker=shadow)





@app.route("/edit_shadow/<username>/<shadow_id>", methods = ['GET', 'POST'])
def edit_shadow(username, shadow_id):
  if request.method == 'GET':
    client = Users.query.filter_by(username = username).first()
    all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    
    return render_template('editingShadow.html', user=client,all_trackers=all_shadows, tracker=shadow)
  if request.method == 'POST':
    shadow_name = request.form['Tracker_name']
    about = request.form['Description']
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    shadow.shadow_name=shadow_name
    shadow.about=about
    db.session.commit()
    return redirect(f'/{username}/dashboard')





@app.route("/delete_shadow/<username>/<shadow_id>", methods = ['GET', 'POST'])
def delete_shadow(username, shadow_id):
  shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
  all_logs = Logs.query.filter_by(shadow_id=shadow.shadow_id).all()
  if all_logs:
    for i in all_logs:
      db.session.delete(i)
  db.session.delete(shadow)
  db.session.commit()
  return redirect(f'/{username}/dashboard')





@app.route("/edit_log/<username>/<shadow_id>/<log_id>", methods = ['GET', 'POST'])
def editing_log(username,shadow_id, log_id):
  if request.method == 'GET':
    client = Users.query.filter_by(username = username).first()
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    all_logs = Logs.query.filter_by(shadow_id=shadow.shadow_id).all()
    all_shadows = ShadowManager.query.filter_by(user_id=client.user_id).all()
    
    
    log = Logs.query.filter_by(log_id=log_id).first()
    
    return render_template(f'edit{shadow.shadow_type}.html', user=client,all_logs=all_logs, all_trackers=all_shadows, tracker=shadow, log=log)
  if request.method == 'POST':
    value = request.form['value']
    note = request.form['note']
    log = Logs.query.filter_by(log_id=log_id).first()
    shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
    log.value = value 
    log.note = note
    db.session.commit()
    return redirect(f'/{username}/{shadow_id}')





@app.route("/delete_log/<username>/<shadow_id>/<log_id>", methods = ['GET', 'POST'])
def delete_log(username,shadow_id, log_id):
  log = Logs.query.filter_by(log_id=log_id).first()
  db.session.delete(log)
  db.session.commit()
  return redirect(f'/{username}/{shadow_id}')



@app.route('/logout')
def logout():
	return redirect("/")



@app.route("/graph/<username>/<shadow_id>", methods=['GET', 'POST'])
def graph(username, shadow_id):
  
  
  shadow = ShadowManager.query.filter_by(shadow_id=shadow_id).first()
  name=shadow.shadow_name
  all_logs = Logs.query.filter_by(shadow_id=shadow.shadow_id).all()
  
  
  label=[]
  value=[]
  
  if shadow.shadow_type=="Numerical":
    for i in all_logs:
      label.append(i.time)
      value.append(float(i.value))
    plt.figure()
    
    ax = plt.axes()
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title(f'{name} graph', color='white')
    plt.xticks(rotation=90)
    plt.ylabel('Daily value', color='white')
    plt.xlabel('Time', color='white')
    plt.plot(label, value, 'r')
    plt.savefig(f'static/{name}.png',transparent=True, bbox_inches="tight")
    
  
  elif shadow.shadow_type=="Boolean" or shadow.shadow_type=="Multiple Choice":
    for i in all_logs:
      value.append(str(i.value))
      label.append(i.time)
     
    plt.figure()
    
    ax = plt.axes()

    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title(f'{name} graph', color='white')
    plt.ylabel('Status', color='white')
    plt.xlabel('Time', color='white')
    plt.xticks(rotation=90)
    plt.plot(label, value, 'r')
    plt.savefig(f'static/{name}.png',transparent=True, bbox_inches="tight")
    
  return redirect(f'/{username}/{shadow_id}')