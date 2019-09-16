from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    code = Column(String(4), unique=True)
    url_base = Column(String(150))
    baseurl = synonym("url_base")
    careers = relationship("Career", lazy="dynamic")

    def __str__(self):
        return ("name: " + self.name
                + ", code: " + self.code)


class Career(Base):
    __tablename__ = "careers"

    code = Column(String(15), primary_key=True)
    name = Column(String(100))
    url_base = Column(String(150))
    baseurl = synonym("url_base")
    id_university = Column(Integer, ForeignKey("universities.id"))
    subjects = relationship('Subject', secondary='careers_subjects', back_populates="careers")

    def __init__(self, scheme):
        self.code = scheme['code']
        self.name = scheme['name']
        self.baseurl = scheme['baseurl']

    def __str__(self):
        return ("code: " + self.code
                + ", name: " + self.name
                + ", url_base: " + self.url_base)


class Subject(Base):
    __tablename__ = "subjects"

    code = Column(String(15), primary_key=True)
    name = Column(String(100))
    credits = Column(Float)
    course = Column(Integer)
    period = Column(String(1))
    docencia = Column(String(15))
    careers = relationship("Career", secondary='careers_subjects', back_populates="subjects")

    def __init__(self, scheme):
        self.code = scheme['code']
        self.name = scheme['name']
        self.credits = scheme['credits']
        self.course = scheme['course']
        self.period = scheme['period']
        self.type = scheme['type']
        self.docencia = scheme['docencia']

    def __str__(self):
        return ("code: " + self.code
                + ", name: " + self.name
                + ", credits: " + str(self.credits))


careers_subjects = Table('careers_subjects', Base.metadata,
    Column('career_code', String(15), ForeignKey('careers.code'), primary_key=True),
    Column('subject_code', String(15), ForeignKey('subjects.code'), primary_key=True)
)
