from flask import Flask, render_template, request, redirect
import bh_db

app = Flask(__name__)
is_admin = ''


@app.route("/", methods=['GET', 'POST'])
def index():
    global is_admin
    if request.method == 'GET':
        workers_ = bh_db.get_dep_workers_list(True)
        return render_template('bh_form.html', workers=workers_, is_admin=is_admin)
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        if form_data['action'] == 'Submit_admin':
            if form_data['pw'] == '123':
                is_admin = 'True'
                workers_ = bh_db.get_dep_workers_list(True)
                return render_template('bh_form.html', workers=workers_, is_admin=is_admin)
            else:
                return '<h1>Wrong password!</h1>'
        else:
            bh_db.add_bh(form_data['workers'], form_data['data'], form_data['horas'], form_data['desc'], False)
            return render_template('new_entry.html', form_data=form_data, is_admin=is_admin)


@app.route("/admin")
def index_admin():
    return render_template('bh_admin.html', is_admin=is_admin)


@app.route("/update_chk", methods=['GET'])
def update_chk():
    chk_id = request.args.get('chkid')
    chk = request.args.get('ischecked')
    bh_db.update_chk(chk_id, chk)
    entradas_, soma_, soma_approved_ = get_bh(request.args.get('worker_n'))
    return str(soma_approved_)


@app.route("/update_bh", methods=['POST'])
def update_bh():
    form_data = request.form
    print(form_data)
    bh_db.update_bh(form_data['chkid'], form_data['data'], form_data['horas'], form_data['desc'])
    entradas_, soma_, soma_approved_ = get_bh(form_data['worker_n'])
    return str(soma_approved_)


@app.route('/workers')
def workers_list():
    workers_ = bh_db.get_dep_workers_list(False)
    return render_template('workers_list.html', workers=workers_, is_admin=is_admin)


@app.route('/banco_horas', methods=['GET', 'POST'])
def bancohoras_list():
    workers_ = bh_db.get_dep_workers_list(False)
    if request.method == 'GET':
        worker_name_ = 'Todos'
        entradas_, soma_, soma_approved_ = bh_db.get_bh_all()
        return render_template('bh_list.html', entradas=entradas_, worker_name=worker_name_, workers=workers_, is_admin=is_admin)
    if request.method == 'POST':
        form_data = request.form
        worker_name_ = form_data['workers']
        entradas_, soma_, soma_approved_ = get_bh(worker_name_)
        return render_template('bh_list.html', entradas=entradas_, worker_name=worker_name_, workers=workers_, soma=soma_, soma_approved=soma_approved_, is_admin=is_admin)


def get_bh(worker_name):
    if worker_name == 'Todos':
        entradas_, soma_, soma_approved_ = bh_db.get_bh_all()
    else:
        entradas_, soma_, soma_approved_ = bh_db.get_bh(worker_name)
    return entradas_, soma_, soma_approved_


if __name__ == "__main__":
    bh_db.connect_db()
    # bh_db.init_workers_db()
    # app.run(host="127.0.0.1", port=8080, debug=True)
    app.run()
