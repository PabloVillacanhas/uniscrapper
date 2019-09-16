from persistence.session import session
from scrappers.usc import USCCareerScrapper, USCSubjectScrapper
from persistence import models


def main():
    if len(session.query(models.University).all()) == 0:
        university = models.University()
        university.name = "Universidad de Santiago de Compostela"
        university.code = "USC"
        university.baseurl = "www.usc.es/graos/es"
        session.add(university)
        session.commit()
    universities = session.query(models.University).all()
    for university in universities:
        career_scrapper = USCCareerScrapper(university.code)
        career_scrapper.execute()
        for career in career_scrapper.getData():
            existing_career = session.query(models.Career).filter(models.Career.code == career.code).one_or_none()
            if existing_career is not None:
                university.careers.append(existing_career)
            else:
                university.careers.append(career)
            subject_scrapper = USCSubjectScrapper(career.baseurl, career.name)
            subject_scrapper.execute()
            for subject in subject_scrapper.getData():
                existing_subject = session.query(models.Subject).filter(models.Subject.code == subject.code).one_or_none()
                if existing_subject is not None:
                    career.subjects.append(existing_subject)
                else:
                    career.subjects.append(subject)
        session.merge(university)
    session.commit()
    # uscscrapper = USCSubjectScrapper(url, "CC").execute()

if __name__ == "__main__":
    main()
