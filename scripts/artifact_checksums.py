"""Pinned size and at least one expected checksum; never infer a provider MD5."""
import re


def validate_expected(expected):
    if not isinstance(expected,dict) or set(expected)-{'bytes','md5','sha256'}:raise ValueError('Checksum schema')
    if type(expected.get('bytes')) is not int or expected['bytes']<0:raise ValueError('Nonnegative integer size required')
    supplied=False
    for key,length in [('md5',32),('sha256',64)]:
        value=expected.get(key)
        if value is not None:
            if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{'+str(length)+'}',value):raise ValueError('Malformed expected '+key)
            supplied=True
    if not supplied:raise ValueError('At least one pinned checksum required')


def check(expected,*,size,md5,sha256):
    validate_expected(expected)
    if size!=expected['bytes']:raise ValueError('Size mismatch')
    for key,actual in [('md5',md5),('sha256',sha256)]:
        if expected.get(key) is not None and expected[key]!=actual:raise ValueError('Hash mismatch: '+key)
