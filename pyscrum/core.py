#--coding: utf8--


class Task(object):
    """
    Задача для разработчика.
    """
    NEW, WORK, DONE = range(3)

    def __init__(self, title, state, person=None, points=None):
        self.title = title
        self.state = state
        self.person = person
        self.points = points


class Story(object):
    """
    История в scrum-терминологии.
    """
    def __init__(self, title, description=None, tasks=None):
        self.title = title
        self.description = description
        self.tasks = []
        self.tasks.extend(tasks)

    def points(self):
        """
        Суммарная оценка трудоемкости по всем задачам.
        """
        return sum(t.points for t in self.tasks)

    def _filter_tasks_by_state(self, state):
        return [t for t in self.tasks
                if t.state == state]

    def new_tasks(self):
        return self._filter_tasks_by_state(Task.NEW)

    def work_tasks(self):
        return self._filter_tasks_by_state(Task.WORK)

    def done_tasks(self):
        return self._filter_tasks_by_state(Task.DONE)

    def is_new(self):
        """
        Все задачи истории - новые.
        """
        return len(self.tasks) == len(self.new_tasks())

    def is_done(self):
        """
        Все задачи выполнены.
        """
        total = len(self.tasks)
        return total > 0 and total == len(self.done_tasks())

    def new_points(self):
        """
        Сумма оценок по новым задачам.
        """
        return sum(t.points for t in self.new_tasks())

    def work_points(self):
        return sum(t.points for t in self.work_tasks())

    def done_points(self):
        return sum(t.points for t in self.done_tasks())


class Board(object):
    """
    Доска с историями.
    """
    def __init__(self, title, stories):
        self.title = title
        self.stories = stories

    def new_points(self):
        return sum(s.new_points() for s in self.stories)

    def work_points(self):
        return sum(s.work_points() for s in self.stories)

    def done_points(self):
        return sum(s.done_points() for s in self.stories)

    def points(self):
        return sum(s.points() for s in self.stories)

    def progress(self):
        total = self.points()
        if total:
            return float(self.done_points()) / float(total) * 100
        else:
            return 0
