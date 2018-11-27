import hashlib

from core.foundation.utils import date_utils
from core.foundation.utils.date_utils import Y_M_D_H_M


def gen_reference_no(string):
    date_time = date_utils.current(Y_M_D_H_M)
    return hashlib.md5((string + date_time).encode('utf-8')).hexdigest()
