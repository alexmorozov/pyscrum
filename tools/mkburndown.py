#!/usr/bin/env python
#--coding: utf8--

import sys
import re
import os.path
from datetime import datetime, timedelta
import shlex
import subprocess
import json

from jinja2 import Environment, PackageLoader

from pyscrum.loaders import StringRstLoader


def guess_dates(filename):
    name, _ = os.path.splitext(os.path.basename(filename))
    matches = re.findall(r'([\d\.]{8,10})', name)
    if matches and len(matches) == 2:
        return [datetime.strptime(x, '%d.%m.%y').date() for x in matches]
    raise ValueError(('Invalid filename: should contain a date range '
                      'dd.mm.yy-dd.mm.yy'))


def points(filename, date):
    """
    Получить общее количество пунктов и кол-во выполненных на определенную
    дату.
    """
    cmd = "git show '@{%s}':%s" % (date.strftime('%Y.%m.%d'),
                                   os.path.basename(filename))
    args = shlex.split(cmd)
    p = subprocess.Popen(args, cwd=os.path.dirname(filename),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.returncode != 0:
        raise Exception('Something gone wrong with git: "%s"' % err)
    loader = StringRstLoader()
    board = loader.get_board(output)

    return board.points, board.done_points


if __name__ == '__main__':
    filename = sys.argv[1]
    start, end = guess_dates(filename)
    d = start
    today = datetime.today().date()
    done, days, total_max = [], [], 0
    while d <= end:
        if d <= today:
            total, day_done = points(filename, d)
            total_max = max(total, total_max)
            done.append(day_done)
        days.append(d.strftime('%d.%m'))
        d += timedelta(days=1)

    env = Environment(loader=PackageLoader('pyscrum'))
    template = env.get_template('burndown.html')
    context = {
        'done': json.dumps(done),
        'total': total_max,
        'days': json.dumps(days),
        'title': os.path.basename(filename),
    }
    print template.render(**context).encode('utf-8')
