
import socket
import utils
import logging

HOST = ''

util_functions = {
    value: getattr(utils, value) for value in dir(utils)
    if '__' not in value and callable(getattr(utils, value))
}


def list_functions(command):
    """Return list of available functions."""
    return ', '.join(util_functions.keys())#.encode()


util_functions['list'] = list_functions


def process_data(data):
    if ':' in data:
        func, command = data.split(': ', 1)
    else:
        func = data
        command = ''
    if '??' in func:
        func = func.strip("?")
        logging.debug(f'Returning help for {func}.')
        if util_functions[func].__doc__:
            return util_functions[func].__doc__.encode()
        else:
            return b'No documentation found.'
    if func not in util_functions:
        logging.debug(f'Invalid function!')
        return b'Invalid command.'
    logging.debug(f'Running "{func}" with "{command}".')
    return util_functions[func](command)


if __name__ == '__main__':


    PORT = 9201

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] - %(message)s'
    )

    hostname = socket.gethostname()
    my_ip = socket.gethostbyname(hostname)

    logging.info(
        f'Starting remote-control server on {hostname} ({my_ip}:{PORT})...')

    logging.debug(f'Available functions: {list(util_functions.keys())}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            logging.info('Waiting for clients...')
            conn, addr = s.accept()

            with conn:
                logging.info(f'Connected by: {addr}.')
                while True:
                    logging.debug('Waiting for message...')
                    data = conn.recv(1024).decode()
                    if not data:
                        logging.info('Client disconnected.')
                        break
                    logging.info('Processing command.')
                    logging.debug(f'Received: {data}.')
                    try:
                        retvalue = process_data(data)
                        logging.debug(f'Sending response: {retvalue}')
                        conn.sendall(retvalue)
                    except Exception as e:
                        logging.exception(e)
                        conn.sendall(b'Server error.')
                    logging.info('Response sent.')