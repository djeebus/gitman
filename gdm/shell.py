"""Utilities to call shell programs."""

import os
import sys
import logging

from sh import Command, ErrorReturnCode

from . import common

CMD_PREFIX = "$ "
OUT_PREFIX = "> "

log = logging.getLogger(__name__)


def call(name, *args, ignore=False, catch=True, capture=False, visible=True):
    """Call a shell program with arguments."""
    msg = CMD_PREFIX + ' '.join([name] + list(args))
    if visible:
        common.show(msg)
    else:
        log.debug(msg)

    if name == 'cd' and len(args) == 1:
        return os.chdir(args[0])

    try:
        program = Command(name)
        if capture:
            line = program(*args).strip()
            log.debug(OUT_PREFIX + line)
            return line
        else:
            for line in program(*args, _iter='err'):
                log.debug(OUT_PREFIX + line.strip())
    except ErrorReturnCode as exc:
        msg = "\n  IN: '{}'{}".format(os.getcwd(), exc)
        if ignore:
            log.debug("Ignored error from call to '%s'", name)
        elif catch:
            sys.exit(msg)
        else:
            raise common.CallException(msg)


def mkdir(path):
    call('mkdir', '-p', path)


def cd(path, visible=True):
    call('cd', path, visible=visible)


def ln(source, target):
    dirpath = os.path.dirname(target)
    if not os.path.isdir(dirpath):
        mkdir(dirpath)
    call('ln', '-s', source, target)


def rm(path):
    call('rm', '-rf', path)
