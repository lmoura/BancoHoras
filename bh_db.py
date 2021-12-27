from peewee import *
import datetime
from icecream import ic

date_comb = datetime.date(1, 1, 1)

workers_tbl = "workers_tbl"
bh_tbl = "bh_tbl"
db = SqliteDatabase('db/bh.db')


def connect_db():
    db.connect()
    db.create_tables([Worker, BH])


class Worker(Model):
    name = CharField(unique=True)
    department = CharField()
    active = BooleanField()

    class Meta:
        database = db
        table_name = workers_tbl


class BH(Model):
    worker_id = ForeignKeyField(Worker, backref='turnos')
    data_pedido = DateField()
    data = DateField()
    duration = TimeField()
    desc = CharField()
    approved = BooleanField()

    class Meta:
        database = db
        table_name = bh_tbl


def add_worker(worker):
    # {'nome': 'Filipa', 'department': 'Rec', 'active': true}
    a_worker = Worker.get_or_none(Worker.name == worker.get('nome'))
    if a_worker is not None:  # Verificar se o worker existe. Se existir atualizar os dados
        a_worker.department = worker.get('department')
        a_worker.active = worker.get('active')
        a_worker.save()
    else:  # Se não existe, criá-lo
        a_worker = Worker.create(name=worker.get('nome'), department=worker.get('department'),
                                 weekly_hours=worker.get('active'))

    return a_worker


def get_dep_workers_list(active_):
    if active_:
        return Worker.select().where(Worker.active == active_).order_by(Worker.name)
    else:
        return Worker.select().order_by(Worker.name)


def add_bh(worker_name, date_, duration_, desc_, approved_):
    a_worker = Worker.get_or_none(Worker.name == worker_name)

    if a_worker is not None:  # Verificar se o worker existe
        uma_entrada = BH.get_or_none((BH.worker_id == a_worker) & (BH.data == date_))
        if uma_entrada is not None:  # Verificar se o BH existe. se existir atualiza-se
            uma_entrada.duration = duration_
            uma_entrada.desc = desc_
            uma_entrada.approved = approved_
            uma_entrada.save()
        else:  # Se não existir cria-se
            uma_entrada = BH.create(
                worker_id=a_worker,
                data_pedido=datetime.date.today(),
                data=date_,
                duration=duration_,
                desc=desc_,
                approved=approved_)
        return uma_entrada

    else:
        # TODO: Acrescentar Worker
        print("add_bh: I don't now this guy! " + worker_name)
        return None


def get_bh(worker_name):
    a_worker = Worker.get_or_none(Worker.name == worker_name)
    if a_worker is not None:  # Verificar se o worker existe
        soma = BH.select(fn.SUM(BH.duration)).where(BH.worker_id == a_worker.id).scalar()
        soma_approved = BH.select(fn.SUM(BH.duration)).where(BH.worker_id == a_worker.id, BH.approved == 1).scalar()
        if soma_approved is None:
            soma_approved = 0
        print(f"soma_approved: {soma_approved}")
        return BH.select().where(BH.worker_id == a_worker.id).order_by(BH.data), soma, soma_approved
    else:
        print("get_bh: I don't now this guy! " + worker_name)
        return None


def init_db():
    db.drop_tables(Worker)
    db.create_tables(Worker)
    db.drop_tables(BH)
    db.create_tables(BH)


#  ################### Utils #####################################
def time_to_float(time):
    return time.hour + time.minute / 60


def str_to_time(time_str):
    # ic("str_to_time: " + time_str)
    time_format = '%H:%M'
    time_parts = time_str.split(":")
    if len(time_parts) == 1:
        time_format = '%H'

    if time_parts[0] == '24':
        time_str = '0:00'
        time_format = '%H:%M'

    return datetime.datetime.strptime(time_str, time_format).time()


#  ################## DEBUG #######################################
def init_workers_db():
    # db.drop_tables(BH)
    # db.create_tables(BH)

    # db.drop_tables(Worker)
    # db.create_tables(Worker)

    workers = (
        ("Filipa", 'Rec'),
        ("Ângela", 'Rec'),
        ("Cátia M", 'Rec'),
        ("Rita P", 'Aux'),
        ("Marisa", 'Aux'),
        ("Giovanna", 'Aux'),
        ("Andreia P", 'Aux'),
        ("Vera", 'Aux'),
        ("Ana Marlene", 'Enf'),
        ("Andreia R", 'Enf'),
        ("Catarina M", 'Méd'),
        ("Catarina A", 'Méd'),
        ("André", 'Méd'),
        ("Kiko", 'Méd'),
        ("Ivo", 'Méd'),
        ("Sofia", 'Méd'),
        ("Bernardo", 'Méd'),
        ("Joana", 'Loj'),
        ("Ana C", 'Loj'),
        ("Catarina", 'Loj'),
        ("Rosa", 'Loj')
    )

    for worker in workers:
        one_worker = Worker(name=worker[0], department=worker[1], active=True)
        one_worker.save()
