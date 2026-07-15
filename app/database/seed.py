from app.database.connection import get_session
from app.database.models import Machine



def seed():

    session = get_session()


    machines = [

        Machine(
            name="Pressa 01",
            status="ACTIVE",
            temperature=65.5
        ),


        Machine(
            name="Robot 02",
            status="STOPPED",
            temperature=40.2
        ),


        Machine(
            name="Forno 03",
            status="ACTIVE",
            temperature=120.8
        )

    ]


    session.add_all(
        machines
    )


    session.commit()

    session.close()



if __name__ == "__main__":

    seed()