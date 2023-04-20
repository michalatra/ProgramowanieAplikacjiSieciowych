import socket
import time

HOST = "127.0.0.1"
PORT = 9801

TEST_MESSAGE_CONTENT_SM = "Test message".encode("utf-8")

RETRY_COUNT = 100000


def perfotm_test():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        start_time = time.time()

        for i in range(RETRY_COUNT):
            client.sendall(TEST_MESSAGE_CONTENT_SM)

        end_time = time.time()

    executionTime = end_time - start_time
    print("Execution time: " + str(executionTime))
    return executionTime


def measure_performance():
    results = []
    for i in range(10):
        results.append(perfotm_test())

    print("Results: " + str(results))
    print("Average execution time: " + str(sum(results) / len(results)))

if __name__ == "__main__":
    measure_performance()