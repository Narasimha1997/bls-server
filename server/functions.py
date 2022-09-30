import os
from typing import Tuple
from blspy import (
    AugSchemeMPL,
    G1Element,
    G2Element,
    PrivateKey,
)

def urandom_bytes() -> bytes:
    return os.urandom(128)

def prepare_env() -> dict:

    env_vars = dict()
    # port
    env_vars['port'] = os.getenv("GRPC_PORT", "8000")

    # private keys (note: Since you are passing the private keys as env, make sure you are mounting those envs to this container by secure means)
    key_map = os.getenv("KEY_MAP", None)
    keys = dict()
    if key_map:
        all_keys = key_map.split("::")
        for key in all_keys:
            splits = key.split("=")
            if len(splits) != 2:
                raise Exception("malformed key mapping string, it should be of the form key_name1=key::key_name2=key::key_name3=key...")
            name, key = splits
            keys[name] = key
    
    env_vars['keys'] = keys
    
    # seed -  this is used for generating new private keys
    seed = os.getenv("KEYGEN_SEED_HEX", urandom_bytes())
    if type(seed) == str:
        seed = seed[2:] if seed.startswith("0x") else seed
        seed = bytes.fromhex(seed)

    env_vars['seed'] = seed
    
    return env_vars


def generate_keypair(env: dict, keep_raw=True):
    seed = env['seed']
    private_key = AugSchemeMPL.key_gen(seed)
    public_key = private_key.get_g1()
    prvk_b, pubk_b = bytes(private_key), bytes(public_key)

    if keep_raw:
        return prvk_b, pubk_b

    return prvk_b.hex(), pubk_b.hex()
