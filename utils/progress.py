import progressbar as pb


class ScrapperProgressBar:

    def __init__(self, n_iter, subjectname):
        self.n_iter = n_iter
        self.iter = 0
        self.description = "Scrapping " + subjectname
        self.timer = None
        self.initialize()

    def initialize(self):
        widgets = [
            self.description,
            pb.Bar(),
            ' (', pb.SimpleProgress(), ') ',
        ]
        self.timer = pb.ProgressBar(widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        self.timer.finish()
