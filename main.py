import uuid

import bluetooth as bt

uuid = uuid.uuid1().__str__()


def __main__():
    # Host bluetooth server
    server = bt.BluetoothSocket(bt.L2CAP)
    server.bind(('', bt.PORT_ANY))
    server.listen(1)

    # Accept connection
    client, address = get_client(server)


def get_client(server):
    """
    Hosts bluetooth server and waits for a client to connect
    :arg server bound and listening SocketServer
    """
    # Advertise to other devices
    bt.advertise_service(server, "Bob", uuid,
                      [uuid, bt.SERIAL_PORT_CLASS],
                      [bt.SERIAL_PORT_PROFILE], description='Robotics Raspberry pi')
    print(f'Awaiting connection on {server.getsockname()[1]}')

    # Accept first client
    client, address = server.accept()
    print(f'Accepted client from {address} {client}')
    bt.stop_advertising(server)

    # Close connections
    server.close()
    return client, address


if __name__ == '__main__':
    __main__()
