from sqlalchemy import Column, Integer, VARCHAR, create_engine, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DropoffTable(Base):
    __tablename__ = 'DropoffTable'
    id = Column(Integer, primary_key=True)
    test_name = Column(VARCHAR, nullable=False)
    date_in = Column(Date, nullable=False)
    instructor_name = Column(VARCHAR, nullable=False)
    initial_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, nullable=False)

class PickupTable(Base):
    __tablename__ = 'PickupTable'
    id = Column(Integer, primary_key=True)
    CE = Column(VARCHAR(1)) # Completed or Expired
    student_name = Column(VARCHAR)
    test_name = Column(VARCHAR) # varchar cause "midterm" can be included
    HN = Column(VARCHAR(1)) # Homework or Notecard
    date_in = Column(Date)
    date_out = Column(Date)
    staff_initial = Column(VARCHAR)
    SFMP = Column(VARCHAR) # Sent or Filed or Mailed or Pickup
    instructor_name = Column(VARCHAR)
    dropoff_id = Column(Integer, ForeignKey('DropoffTable.id'))
    is_resolved = Column(Boolean)


class Connection:
    def __init__(self, file):
        self.engine = create_engine(f'sqlite:///{file}?check_same_thread=False')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def connect(self):
        return self.session
