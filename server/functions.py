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
    seed = os.getenv("KEYGEN_SEED_HEX", urandom_bytes())
    if type(seed) == str:
        seed = seed[2:] if seed.startswith("0x") else seed
        seed = bytes.fromhex(seed)

    env_vars['seed'] = seed
    
    return env_vars


def generate_keypair(env: dict, key_id: str, keep_raw=True):
    seed = env['seed']
    private_key = AugSchemeMPL.key_gen(seed)
    public_key = private_key.get_g1()
    prvk_b, pubk_b = bytes(private_key), bytes(public_key)

    # register the newly generated key
    env['key_store'].put(key_id, prvk_b.hex())

    if keep_raw:
        return pubk_b
    return pubk_b.hex()

