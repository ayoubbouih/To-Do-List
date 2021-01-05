from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.string_field


def menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    try:
        choice = int(input())
        if choice == 0:
            print("Bye!")
            return 0
        elif choice == 1:
            today_task()
        elif choice == 2:
            week_task()
        elif choice == 3:
            all_task()
        elif choice == 4:
            missed_task()
        elif choice == 5:
            add_task()
        elif choice == 6:
            delete_task()
    except ValueError:
        print("you should enter a number")


def add_task():
    print("Enter task")
    task = input()
    print("Enter deadline")
    date = input()
    try:
        new_row = Table(task=task, deadline=datetime.strptime(date, "%Y-%m-%d"))
        session.add(new_row)
        session.commit()
    except (ValueError, TypeError):
        print("error")
    else:
        print("The task has been added!")


def today_task():
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for x in rows:
            print(f"{x.id}. {x.task}")


def week_task():
    for i in range(0, 8):
        day = datetime.today().date() + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == day).order_by(Table.deadline).all()
        print()
        print(f"{day.strftime('%A')} {day.day} {day.strftime('%b')}")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for x in rows:
                print(f"{x.id}. {x.task}")


def all_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for x in rows:
            print(f"{x.id}. {x.task}. {x.deadline.day} {x.deadline.strftime('%b')}")


def missed_task():
    missed = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    print("Missed tasks:")
    if len(missed):
        for x in range(len(missed)):
            print(f"{x}. {missed[x].task}. {missed[x].deadline.day} {missed[x].deadline.strftime('%b')}")
    else:
        print("Nothing is missed!")
    print()

def delete_task():
    print("Choose the number of the task you want to delete:")
    all_task()
    try:
        choice = int(input())
        item = session.query(Table).filter(Table.id == choice).all()
        session.delete(item[0])
        session.commit()
    except:
        print("there is an error occured!")
    else:
        print("The task has been deleted!")


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    if menu() == 0:
        break
