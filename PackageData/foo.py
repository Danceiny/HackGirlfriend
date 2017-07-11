import test
import message
def handle_foo_log_msg(txt):
    print(txt)

import message
def hello(name):
    print("Hello {}".format(name))
message.sub("greet", hello)
message.pub("greet", "lai")

message.sub(test.LOG_MSG, handle_foo_log_msg)

class Some_Class(object):
    somevalue = 10
    def __init__(self):
        self._somevalue = 0
    def get_value(self):
        print self.somevalue
        return self._somevalue
    def set_value(self, value):
        self._somevalue = value
    def del_attr(self):
        del self._somevalue
    x = property(get_value, set_value, del_attr, "I am the ''x' property.")
s = Some_Class()
print dir(s)
print s.get_value()
print s.somevalue
s.somevalue = 10000

print s.somevalue

s2 = Some_Class()
print s2.somevalue