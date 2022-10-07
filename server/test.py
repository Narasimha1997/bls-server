import rpc
import types_pb2
import grpc
import time
from services_pb2_grpc import BLSSigningStub


with open('/tmp/keys.json', 'w') as key_store_writer:
    key_store_writer.write("{}")

messages = [
    b"this is a no man's land"
]

messages_hex = [m.hex() for m in messages]


def run_in_server_context(function):
    server = rpc.init_rpc_server(8000, 1)
    server.start()

    time.sleep(5)

    with grpc.insecure_channel('localhost:8000') as channel:
        function(channel)


def test_keypairs_generation():

    def test_function(channel: grpc.Channel):
        stub = BLSSigningStub(channel)

        # 1.
        # generate and register a new public-private key pair
        response = stub.GenerateKeypairRaw(
            types_pb2.GenerateKeypairRequestRaw(seed=b'', key_id="test-key"))

        # public key will be sent back in the response, private key will be stored in the key-store
        assert response.success, "failed to generate key-pair {}".format(
            response.error_message)
        # public key will be 48 bytes
        assert len(
            response.public_key) == 48, "invalid public key, the size of public key must be 48 bytes"

        public_key = response.public_key

        # 2.
        # if we make a RPC call with same already existing key_id, we will get the public key from the key-store and no new key-pair will be created
        response = stub.GenerateKeypairRaw(
            types_pb2.GenerateKeypairRequestRaw(seed=b'', key_id="test-key"))

        # the obtained public key will be equal to the public key obtained in the step 1 because we are using the same `key-id`
        assert public_key == response.public_key, "invalid public key, the already existing private key generated a new public key"

        # 3.
        # generate another key-pair with a custom seed
        response = stub.GenerateKeypairRaw(
            types_pb2.GenerateKeypairRequestRaw(seed=b'1' * 32, key_id="test-key-2"))
        # it's public key will be different from the old ones
        assert response.success and response.public_key != public_key, "key generator generated the same key even when a seed was passed"

        # 4.
        # generate another key-pair with a seed < 32 bytes
        response = stub.GenerateKeypairRaw(
            types_pb2.GenerateKeypairRequestRaw(seed=b'1' * 20, key_id="test-key-2"))
        # should throw an error for seed length < 32
        assert not response.success, "server did not throw error for key"

        # 5
        # call GenerateKeypairHex to get the hex representation of the public key
        response = stub.GenerateKeypairHex(types_pb2.GenerateKeypairRequestHex(seed=b'', key_id="test-key"))
        # check if the hex public key is same as the bytes key obtained in step 1
        assert bytes.fromhex(response.public_key) == public_key, "Invalid hex key {}".format(response.public_key)

    run_in_server_context(test_function)

