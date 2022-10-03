import os
from typing import Tuple
from blspy import (
    AugSchemeMPL,
    G1Element,
    G2Element,
    PrivateKey,
)

import backends

def urandom_bytes() -> bytes:
    return os.urandom(128)

def prepare_env() -> dict:

    env_vars = dict()
    # port
    env_vars['port'] = os.getenv("GRPC_PORT", "8000")

    key_vars = os.getenv("KEY_STORAGE_PARAMETERS", None)
    params = dict()
    if key_vars:
        all_keys = key_vars.split("::")
        for key in all_keys:
            splits = key.split("=")
            if len(splits) != 2:
                raise Exception("malformed parameters string, it should be of the form key_name1=value::key_name2=value::key_name3=vakue...")
            name, key = splits
            params[name] = key
    
    env_vars['keystore_backend'] = backends.FileStorageBackend(**params)
    
    # seed -  this is used for generating new private keys
    env_vars['seeder'] = urandom_bytes
    
    return env_vars


def generate_keypair(env: dict, key_id: str, seed: bytes, keep_raw=True):
    seed = env['seeder']() if len(seed) == 0 else seed
    private_key = AugSchemeMPL.key_gen(seed)
    public_key = private_key.get_g1()
    prvk_b, pubk_b = bytes(private_key), bytes(public_key)

    # register the newly generated key
    env['keystore_backend'].put(key_id, prvk_b.hex())

    if keep_raw:
        return pubk_b
    return pubk_b.hex()

def sign_data(env: dict, key_id: str, message, raw = True):
    key = env['keystore_backend'].get(key_id)

    key = bytes.fromhex(key[2:]) if key.startswith("0x") else bytes.fromhex(key)

    if not raw:
        message = bytes.fromhex(message[2:]) if message.startswith("0x") else bytes.fromhex(message)
    
    # sign
    sk = PrivateKey.from_bytes(key)
    signature = AugSchemeMPL.sign(sk, message)
    if raw:
        return bytes(signature)
    return bytes(signature).hex()

def verify_signature(pk, message, signature, raw=True):

    if not raw:
        pk = bytes.fromhex(pk[2:]) if pk.startswith("0x") else bytes.fromhex(pk)
        message = bytes.fromhex(message[2:]) if message.startswith("0x") else bytes.fromhex(message)
        signature = bytes.fromhex(signature[2:]) if signature.startswith("0x") else bytes.fromhex(signature)
    
    # verify
    pk = G1Element.from_bytes(pk)
    signature = G2Element.from_bytes(signature)
    return AugSchemeMPL.verify(pk, message, signature)
