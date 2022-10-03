import grpc
from concurrent import futures
import time

import services_pb2_grpc 
import types_pb2
import functions

env = functions.prepare_env()

class BLSServicer(services_pb2_grpc.BLSSigningServicer):
    
    def GenerateKeypairRaw(self, request, context):
        try:
            public_key = functions.generate_keypair(env, request.key_id, request.seed, True)
            return types_pb2.GenerateKeypairResponseRaw(
                success=True,
                public_key=public_key,
                error_message=''
            )
        except Exception as e:
            return types_pb2.GenerateKeypairResponseRaw(
                success=False,
                public_key=b'',
                error_message=str(e)
            )
    
    def GenerateKeypairHex(self, request, context):
        try:
            public_key = functions.generate_keypair(env, request.key_id, request.seed, False)
            return types_pb2.GenerateKeypairResponseHex(
                success=True,
                public_key=public_key,
                error_message=''
            )
        except Exception as e:
            return types_pb2.GenerateKeypairResponseHex(
                success=False,
                public_key=b'',
                error_message=str(e)
            )

    def SignRaw(self, request, context):
        try:

            signature = functions.sign_data(env, request.key_identity, request.message, True)
            return types_pb2.SignResponseRaw(
                success=True,
                signature=signature,
                error_message=''
            )

        except Exception as e:
            return types_pb2.SignResponseRaw(
                success=False,
                signature=b'',
                error_message=str(e)
            )


    def SignHex(self, request, context):
        try:
            signature = functions.sign_data(env, request.key_identity, request.message, False)
            return types_pb2.SignResponseHex(
                success=True,
                signature=signature,
                error_message=''
            )

        except Exception as e:
            return types_pb2.SignResponseHex(
                success=False,
                signature='',
                error_message=str(e)
            )
    

def run_server():
    port = env['port']
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_BLSSigningServicer_to_server(BLSServicer(), server)
    server.add_insecure_port('0.0.0.0:{}'.format(port))
    server.start()

    print('started gRPC server at 0.0.0.0:{}'.format(port))

    while True:
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    run_server()