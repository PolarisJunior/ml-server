
from ml_collection import register_algo


# https://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined
class MetaBase(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaBase, cls).__new__(cls, clsname, bases, attrs)
        if newclass.algo_id != -1:
            register_algo(newclass.algo_id, newclass)
        return newclass
    pass

class MlBase(metaclass=MetaBase):
    algo_name = "invalid"
    algo_id = -1

    def run(self):
        raise Exception("No run method defined", self.__class__)
