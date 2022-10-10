# bls-server
A gRPC server written in python that provides BLS (Boneh–Lynn–Shacham) signatures related functionalities like signing, verification and signatures aggregation - used in production at some places. The core BLS implementation is taken from [BLS12-381 C++ library used in Chia-blockchain](https://github.com/Chia-Network/bls-signatures). You can read more about BLS12-381 here - [BLS12-381: New zk-SNARK Elliptic Curve Construction](https://electriccoin.co/blog/new-snark-curve/) and [Pairing-Friendly Curves](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-pairing-friendly-curves-02). 

## Using bls-server as a microservice
The `Dockerfile` used in this repository can be used to build and deploy the server as a container. The server is also completely stateless and can be scaled up and down whenever required without having to worry about the state management.

To build the container image using docker:
```
docker build . -t bls-server:latest
```

To run:
```
docker run --rm -p 8000:8000 -v $PWD/keydir:/keydir --env='KEY_STORAGE_PARAMETERS=file_path=/keydir/keys.json' bls-server:latest
```

## List of available gRPC calls
###  1. Generate a new key-pair (private and public key)
Request format:
```
// get the public key as hex-string
message GenerateKeypairRequestHex {
    bytes seed = 1;
    string key_id = 2;
}

// get the public key as bytes
message GenerateKeypairRequestRaw {
    bytes seed = 1;
    string key_id = 2;
}
```
`seed` is a 32-byte random bytes which is used to generate the private key, if seed is empty server will use `os.urandom()` to generate a random byte sequence as seed.
`key_id` is the unique identifier with which the key can be identified, if `key_id` already exists, instead of generating a new key-pair, the public key will be derived from the existing key and returned.

The keys created using this RPC call will be stored in the key-store (look at key-backend section).

Response format:
```
// response when GenerateKeypairRaw is invoked
message GenerateKeypairResponseRaw {
    bool success = 1;
    bytes public_key = 2;
    string error_message = 3;
}

// response when GenerateKeypairHex is invoked
message GenerateKeypairResponseHex {
    bool success = 1;
    string public_key = 2;
    string error_message = 3;
}
```
`error_message` is non-empty when `success` is `false`.

gRPC calls:
```
// raw
rpc GenerateKeypairRaw (bls_proto.GenerateKeypairRequestRaw) returns(bls_proto.GenerateKeypairResponseRaw);
// hex
rpc GenerateKeypairHex (bls_proto.GenerateKeypairRequestHex) returns(bls_proto.GenerateKeypairResponseHex);
```

### 2. Sign messages using the private key
Request format:
```
// sign a raw bytes message, returns a bytes signature
message SignRequestRaw {
    string key_identity = 1;
    bytes message = 2;
}

// sign a hex message, returns a hex signature
message SignRequestHex {
    string key_identity = 1;
    string message = 2;
}
```
Here the `key_identity` is a unique key which we used when creating calling `GenerateKeypairRaw` or `GenerateKeypairHex` to identify a private key.

Response format:
```
// response when SignRaw is invoked
message SignResponseRaw {
    bool success = 1;
    bytes signature = 2;
    string error_message = 3;
}

// response when SignHex is invoked
message SignResponseHex {
    bool success = 1;
    string signature = 2;
    string error_message = 3;
}
```
`error_message` is non-empty when `success` is `false`.

gRPC calls:
```
// raw
rpc SignRaw (bls_proto.SignRequestRaw) returns(bls_proto.SignResponseRaw);
// hex
rpc SignHex (bls_proto.SignRequestHex) returns(bls_proto.SignResponseHex);
```

### 3. Verifying signatures
Request format:
```
// all the fields in bytes
message VerifyRequestRaw {
    bytes public_key = 1;
    bytes message = 2;
    bytes signature = 3;
}

// all the fields in hex
message VerifyRequestHex {
    string public_key = 1;
    string message = 2;
    string signature = 3;
}
```
`public_key` is the public key of the private key used for signing, `message` is the message which was signed and `signature` is the signature obtained as a result of signing `message` using the private key by the server (response of `SignRaw` or `SignHex `).

Response format:
```
message VerifyResponse {
    bool success = 1;
    bool is_verified = 2;
    string error_message = 3;
}
```
`error_message` is non-empty when `success` is `false`.

gRPC calls:
```
// raw
rpc VerifyRaw (bls_proto.VerifyRequestRaw) returns(bls_proto.VerifyResponse);
// hex
rpc VerifyHex (bls_proto.VerifyRequestHex) returns(bls_proto.VerifyResponse);
```

### 4. Create aggregate signatures
Request format:
```
// send signatures as bytes, the aggregated signature will also be returned as bytes
message AggregateRequestRaw {
    repeated bytes signatures = 1;
}

// send signatures as hex, the aggregated signature will also be returned as hex
message AggregateRequestHex {
    repeated string signatures = 2;
}
```
`signatures` is an array of signatures that needs to be aggregated into a single signature.

Response format:
```
// returned when AggregateRaw is called
message AggregateResponseRaw {
    bool success = 1;
    bytes signature = 2;
    string error_message = 3;
}

// returned when AggregateHex is called
message AggregateResponseHex {
    bool success = 1;
    string signature = 2;
    string error_message = 3;
}
```
`error_message` is non-empty when `success` is `false`.

gRPC calls:
```
// raw
rpc AggregateRaw (bls_proto.AggregateRequestRaw) returns(bls_proto.AggregateResponseRaw);// hex
// hex
rpc AggregateHex (bls_proto.AggregateRequestHex) returns(bls_proto.AggregateResponseHex);
```

### 5. Verify aggregated signatures
Request format:
```
// all the fields are in bytes
message VerifyAggregateRequestRaw {
    repeated bytes public_keys = 1;
    repeated bytes messages = 2; 
    bytes aggregate_signature = 3;
}

// all the fields are in hex
message VerifyAggregateRequestHex {
    repeated string public_keys = 1;
    repeated string messages = 2; 
    string aggregate_signature = 3;
}
```
`public_keys` contains list of public keys whose private keys were used for signing the messages - the public keys has to be passed per each message in the `messages` field. `aggregate_signature` is the aggregated signature (usually obtained when calling `AggregateRaw` and `AggregateHex`.

Response format:
```
message VerifyAggregateResponse {
    bool success = 1;
    bool is_verified = 2;
    string error_message = 3;
}
```

gRPC calls:
```
// raw
rpc VerifyAggregatedRaw (bls_proto.VerifyAggregateRequestRaw) returns (bls_proto.VerifyAggregateResponse);
// hex
rpc VerifyAggregatedHex (bls_proto.VerifyAggregateRequestHex) returns (bls_proto.VerifyAggregateResponse);
```

## Private-Key storage backend
The server doesn't provide any de-factor storage for private keys because different people might expect different levels of security while storing the keys. The codebase in the repository provides `FileStorageBackend` which stores all the private keys un-encrypted in a JSON file - this is not recommended to be used in production and must be considered only for the sake of reference. The backend provides a simple base class that any storage implementation has to override to implement it's own functionality. The base class is shown below:

```python3
class PrivateKeyBackend:

    # the custom parameters provided in the  env will be passed during the init
    def __init__(self, **kwargs):
        pass

    # `put` will be called when a new key needs to be saved, return `PrivateKeyBackendPutException` if something fails while put
    def put(self, key_id: str, key: str):
        pass

    # `get` will be called when obtaining the private key from the storage, return `PrivateKeyBackendGetException` if something fails while get
    def get(self, key_id):
        pass
```
The definitions of `PrivateKeyBackendPutException` and `PrivateKeyBackendGetException` are as shown below:
```python3
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
```
The `PrivateKeyBackendPutException` can also be used to supply the existing `key` if the `key_id` is already present. Look at the implementation of `FileStorageBackend` for more.

## Running tests
Tests can be executed locally to validate the functionalities, you have to install `pytest` package and `pytest-dependency` plugin to run tests.
```
pip3 install pytest pytest-dependency
```
Now run the tests:
```
pytest server/test.py
```

## Contributing
Feel free to raise issues, make PRs and suggest any changes.