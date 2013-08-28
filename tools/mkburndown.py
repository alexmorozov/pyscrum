#!/usr/bin/env python
#--coding: utf8--

import sys
import re
import os.path
from datetime import datetime, timedelta
from commands import getstatusoutput

from pyscrum.loaders import StringRstLoader


def guess_dates(filename):
    name, _ = os.path.splitext(os.path.basename(filename))
    matches = re.findall(r'([\d\.]{8,10})', name)
    if matches and len(matches) == 2:
        return [datetime.strptime(x, '%d.%m.%y').date() for x in matches]
    raise ValueError(('Invalid filename: should contain a date range '
                      'dd.mm.yy-dd.mm.yy'))


if __name__ == '__main__':
    filename = sys.argv[1]
    start, end = guess_dates(filename)
    d = start
    while d <= end:
        cmd = "git show '@{%s}':%s" % (d.strftime('%Y.%m.%d'),
                                       os.path.basename(filename))
        retval, output = getstatusoutput(cmd)
        if retval != 0:
            raise Exception('Something gone wrong with git: "%s"' % output)
        loader = StringRstLoader()
        board = loader.get_board(output)
        print "%d of %d" % (board.done_points, board.points)
        d += timedelta(days=1)
