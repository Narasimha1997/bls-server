from email import message
from urllib import response
import rpc
import types_pb2
import grpc
import time
from services_pb2_grpc import BLSSigningStub

import pytest


with open('/tmp/keys.json', 'w') as key_store_writer:
    key_store_writer.write("{}")

messages = [
    b"this is a no man's land",
    b"hello, world"
]

messages_hex = [m.hex() for m in messages]


def run_in_server_context(function):
    server = rpc.init_rpc_server(8000, 1)
    server.start()

    time.sleep(5)

    with grpc.insecure_channel('localhost:8000') as channel:
        function(channel)
    
    server.stop(2)

@pytest.mark.dependency()
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
        response = stub.GenerateKeypairHex(
            types_pb2.GenerateKeypairRequestHex(seed=b'', key_id="test-key"))
        # check if the hex public key is same as the bytes key obtained in step 1
        assert bytes.fromhex(response.public_key) == public_key, "Invalid hex key {}".format(
            response.public_key)

    run_in_server_context(test_function)


@pytest.mark.dependency(depends=['test_keypairs_generation'])
def test_signing_and_verification():

    def test_function(channel: grpc.Channel):
        stub = BLSSigningStub(channel)
        raw_message = messages[0]
        hex_message = messages_hex[0]

        # 1
        # sign bytes message
        # sign the message by identifying a pre-registered private key (in test_keypairs_generation)
        response_raw = stub.SignRaw(types_pb2.SignRequestRaw(
            key_identity="test-key", message=raw_message))
        assert response_raw.success, "failed to sign message {}".format(
            response_raw.error_message)

        # 2
        # sign hex message
        # sign the message by identifying a pre-registered private key (in test_keypairs_generation)
        response_hex = stub.SignHex(types_pb2.SignRequestHex(
            key_identity="test-key", message=hex_message))
        assert response_hex.success, "failed to sign message {}".format(
            response_raw.error_message)

        # 3
        # compare the signatures, the hex representation should be same
        assert bytes.fromhex(response_hex.signature) == response_raw.signature

        # 4
        # verify the hex signature
        # get the public key
        response = stub.GenerateKeypairHex(
            types_pb2.GenerateKeypairRequestHex(seed=b'', key_id="test-key"))
        verification_response = stub.VerifyHex(types_pb2.VerifyRequestHex(
            signature=response_hex.signature, message=hex_message, public_key=response.public_key))
        assert verification_response.success and verification_response.is_verified, "failed to verify signature"

        # 5
        # modify the message and signature verification should fail
        hex_message = hex_message + "012a"
        verification_response = stub.VerifyHex(types_pb2.VerifyRequestHex(
            signature=response_hex.signature, message=hex_message, public_key=response.public_key))
        assert verification_response.success and not verification_response.is_verified

    run_in_server_context(test_function)


@pytest.mark.dependency(depends=['test_keypairs_generation'])
def test_aggregate_signing_verification():

    def test_function(channel: grpc.Channel):
        stub = BLSSigningStub(channel)
        # 1
        # Generate all required signatures

        signatures = []

        response_hex = stub.SignHex(types_pb2.SignRequestHex(
            key_identity="test-key", message=messages_hex[0]))
        assert response_hex.success, "failed to sign message {}".format(
            response_hex.error_message)

        signatures.append(response_hex.signature)

        response_hex = stub.SignHex(types_pb2.SignRequestHex(
            key_identity="test-key", message=messages_hex[1]))
        assert response_hex.success, "failed to sign message {}".format(
            response_hex.error_message)

        signatures.append(response_hex.signature)

        response_hex = stub.SignHex(types_pb2.SignRequestHex(
            key_identity="test-key-2", message=messages_hex[0]))
        assert response_hex.success, "failed to sign message {}".format(
            response_hex.error_message)

        signatures.append(response_hex.signature)

        response_hex = stub.SignHex(types_pb2.SignRequestHex(
            key_identity="test-key-2", message=messages_hex[1]))
        assert response_hex.success, "failed to sign message {}".format(
            response_hex.error_message)

        signatures.append(response_hex.signature)

        # 2
        # generate aggregate signature
        response_agg = stub.AggregateHex(
            types_pb2.AggregateRequestHex(signatures=signatures))
        assert response_agg.success, "failed to generate aggregated signature {}".format(
            response_agg.error_message)

        # 3
        # generate aggregated signature using raw bytes
        signatures_raw = [bytes.fromhex(signature) for signature in signatures]
        response_agg_raw = stub.AggregateRaw(
            types_pb2.AggregateRequestRaw(signatures=signatures_raw))
        assert response_agg_raw.success, "failed to generate aggregated signature {}".format(
            response_agg.error_message)

        # 4
        # validate the signatures
        assert bytes.fromhex(
            response_agg.signature) == response_agg_raw.signature, "signatures did not match"

        # 5
        # verify the aggregated signature

        public_keys = []

        response_pk = stub.GenerateKeypairHex(
            types_pb2.GenerateKeypairRequestHex(seed=b'', key_id="test-key"))
        assert response_pk.success, "failed to obtain public key {}".format(
            response_pk.error_message)
        public_keys.extend([response_pk.public_key, response_pk.public_key])

        response_pk = stub.GenerateKeypairHex(
            types_pb2.GenerateKeypairRequestHex(seed=b'', key_id="test-key-2"))
        assert response_pk.success, "failed to obtain public key {}".format(
            response_pk.error_message)
        public_keys.extend([response_pk.public_key, response_pk.public_key])

        all_messages = [messages_hex[0], messages_hex[1],
                        messages_hex[0], messages_hex[1]]

        response = stub.VerifyAggregatedHex(types_pb2.VerifyAggregateRequestHex(
            public_keys=public_keys,
            messages=all_messages,
            aggregate_signature=response_agg.signature
        ))

        assert response.success and response.is_verified, "failed to verify aggregated signature {}".format(
            response.error_message)
    
    run_in_server_context(test_function)