import json
import os


class PrivateKeyBackendPutException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.cause = self.args[0]
        self.key = self.args[1]

    def __str__(self) -> str:
        return "put_error={}".format(self.cause)


class PrivateKeyBackendGetException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.cause = self.args[0]

    def __str__(self) -> str:
        return "get_error={}".format(self.cause)


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
        print(kwargs)
        self.file_path = kwargs.get('file_path', '/tmp/keys.json')
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').write("{}")

    def put(self, key_id: str, key: str) -> str:
        try:
            data = open(self.file_path)
            dict_repr = json.load(data)

            if key_id in dict_repr:
                raise PrivateKeyBackendPutException('key_id={} already found'.format(key_id), dict_repr[key_id])

            dict_repr[key_id] = key
            json.dump(dict_repr, open(self.file_path, 'w'))

        except Exception as e:
            raise PrivateKeyBackendPutException(str(e), e.key)

    def get(self, key_id: str) -> str:
        try:
            data = open(self.file_path)
            dict_repr = json.load(data)

            if key_id not in dict_repr:
                raise Exception('key_id={} not found'.format(key_id))

            return dict_repr[key_id]

        except Exception as e:
            raise PrivateKeyBackendGetException(str(e))
