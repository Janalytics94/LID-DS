import typing

from dataloader.syscall import Syscall
from algorithms.features.base_syscall_feature_extractor import BaseSyscallFeatureExtractor


class ReturnValue(BaseSyscallFeatureExtractor):
    """

    Extract system call return value for specific syscalls.
    Include:
        write and writev are summarized as           write
        read, readv and are summarized as            read
        sendfile as                                  send_socket
        recv as                                      recv_socket
        getdents as                                  get_dents
    Training phase:
        save highest value.
    Extraction phase:
        normalize with highest value of training phase
    """

    def __init__(self):
        super().__init__()
        self._max = {
            'read': 0,
            'write': 0,
            'recv_socket': 0,
            'get_dents': 0,
            'send_socket': 0
        }

    def train_on(self, syscall: Syscall):
        """

        save max value of each specified syscall

        """
        return_value_string = syscall.param('res')
        if return_value_string is not None:
            try:
                current_bytes = int(return_value_string)
                if current_bytes > 1 and current_bytes < 1000000000:
                    if "write" in syscall.name():
                        if current_bytes >= self._max['write']:
                            self._max['write'] = current_bytes
                    elif "sendfile" in syscall.name():
                        if current_bytes >= self._max['send_socket']:
                            self._max['send_socket'] = current_bytes
                    elif "read" in syscall.name():
                        if current_bytes >= self._max['read']:
                            self._max['read'] = current_bytes
                    elif "getdents" in syscall.name():
                        if current_bytes >= self._max['get_dents']:
                            self._max['get_dents'] = current_bytes
                    elif "recv" in syscall.name():
                        # recv msg from socket
                        # bytes received
                        if current_bytes >= self._max['recv_socket']:
                            self._max['recv_socket'] = current_bytes
                    elif "clone" in syscall.name():
                        # open child process
                        pass
                    elif "getcwd" in syscall.name():
                        # get current working directory
                        pass
                    elif "lseek" in syscall.name():
                        # reposition file offset
                        pass
                    elif "fcntl" in syscall.name():
                        # perform action on fd
                        pass
                    elif "futex" in syscall.name():
                        pass
                    else:
                        print(syscall.name(), return_value_string)
            except Exception:
                pass

    def fit(self):
        print(self._max)

    def extract(self, syscall: Syscall) -> typing.Tuple[int, float]:
        """

        extract return value type and normalize with max value of training phase

        """
        return_value_string = syscall.param('res')
        return_type = None
        normalized_bytes = 0
        if return_value_string is not None:
            try:
                current_bytes = int(return_value_string)
                if current_bytes > 1 and current_bytes < 1000000000:
                    if "write" in syscall.name():
                        return_type = 'write'
                    elif "sendfile" in syscall.name():
                        return_type = 'send_socket'
                    elif "read" in syscall.name():
                        return_type = 'read'
                    elif "recv" in syscall.name():
                        return_type = 'recv_socket'
                    elif "getdents" in syscall.name():
                        return_type = 'get_dents'
                    else:
                        pass
                try:
                    if return_type:
                        normalized_bytes = current_bytes/self._max[return_type]
                    else:
                        normalized_bytes = 0
                except ZeroDivisionError:
                    normalized_bytes = 0
            except Exception:
                pass
        return ReturnValue.get_id(), [normalized_bytes]
