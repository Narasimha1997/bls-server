import rpc
import time

def main():
    server = rpc.init_rpc_server(port=rpc.env['port'], max_workers=10)
    server.start()
    print('Running gRPC server at 0.0.0.0:{}'.format(rpc.env['port']))

    while True:
        time.sleep(10000000)

if __name__ == "__main__":
    main()