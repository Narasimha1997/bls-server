#!/bin/bash

PROTO_SOURCE=$PWD/proto
PROTO_DEST=$PWD/server
REQUIREMENTS_DIR=$PWD/requirements.txt

func install_deps() {
    # install all pip dependencies
    pip3 install -r $REQUIREMENTS_DIR
}

function compile_proto_files() {
    # run protobuf compiler over proto files
    protoc -I=$PROTO_SOURCE --python_out=$PROTO_DEST $PROTO_SOURCE/types.proto
    protoc -I=$PROTO_SOURCE --python_out=$PROTO_DEST $PROTO_SOURCE/services.proto
}

# 1.
install_deps

# 2.
compile_proto_files