
import pytest
from coge import main,createParse
import re


@pytest.fixture
def parser():
    return  createParse()
       

def replaceWithCase(content,before,after):
    regex = re.compile(re.escape(before), re.I)
    partial= regex.sub(lambda x: ''.join(d.upper() if c.isupper() else d.lower()
        for c,d in zip(x.group()+after[len(x.group()):], after)), content)
    return partial




def test_replace(parser):
    ret = replaceWithCase("XxXx","xxxx","abcdefghijk")
    assert  ret == "AbCdefghijk"

def test_replace2(parser):
    ret = replaceWithCase("aXxXxa","xxxx","abcdefghijk")
    assert  ret == "aAbCdefghijka"
