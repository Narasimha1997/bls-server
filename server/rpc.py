import grpc

import services_pb2_grpc
import functions

env = functions.prepare_env()

class BLSRPC(services_pb2_grpc.BLSSigningServicer):
    pass