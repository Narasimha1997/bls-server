import json
from os import EX_CANTCREAT

class PrivateKeyBackendPutException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.cause = self.args[0]
    
    def __str__(self) -> str:
        return "put_error={}".format(self.cause)

class PrivateKeyBackendGetException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.cause = self.args[0]
    
    def __str__(self) -> str:
        return super().__str__()


class PrivateKeyBackend:

    def __init__(self, **kwargs) -> None:
        pass

    def put(self, key_id: str, key: str) -> None:
        pass

    def get(self, key_id) -> str:
        pass


class FileStorageBackend(PrivateKeyBackend):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.file_path = kwargs.get('file_path', '/keys.txt')
    
    def put(self, key_id: str, key: str) -> None:
        try:
            data = open(self.file_path)
            dict_repr = json.load(data)

            if key_id in dict_repr:
                raise Exception('key_id={} already found'.format(key_id))
            
            dict_repr[key_id] = key
            json.dump(open(self.file_path, 'w'), dict_repr)

        except Exception as e:
            raise PrivateKeyBackendPutException(str(e))
    
    def get(self, key_id: str) -> str:
        try:
            data = open(self.file_path)
            dict_repr = json.load(data)

            if key_id not in dict_repr:
                raise Exception('key_id={} not found'.format(key_id))
            
            return dict_repr[key_id]

        except Exception as e:
            raise PrivateKeyBackendGetException(str(e))
