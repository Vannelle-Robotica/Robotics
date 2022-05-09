import uuid

from bluetooth import *

uuid = uuid.uuid1().__str__()


def __main__():
    # Host bluetooth server
    server = BluetoothSocket(L2CAP)
    server.bind(('', PORT_ANY))
    server.listen(1)

    # Accept connection
    client, address = get_client(server)


def get_client(server):
    """
    Hosts bluetooth server and waits for a client to connect
    :arg server bound and listening SocketServer
    """
    # Advertise to other devices
    advertise_service(server, "Bob", uuid,
                      [uuid, SERIAL_PORT_CLASS],
                      [SERIAL_PORT_PROFILE], description='Robotics Raspberry pi')
    print(f'Awaiting connection on {server.getsockname()[1]}')

    # Accept first client
    client, address = server.accept()
    print(f'Accepted client from {address} {client}')
    stop_advertising(server)

    # Close connections
    server.close()
    return client, address


if __name__ == '__main__':
    __main__()
