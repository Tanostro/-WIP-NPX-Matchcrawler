import bin.threads as threads
import bin.console.status as status
def main(string):
    splitstr = string.split()
    for value in splitstr:
        if value == "test":
            return string+"(lel)"
        elif value == "shutdown":
            threads.vars.shutdown = True
            threads.server_thread.Thread.server_socket.close()
            return "shutdown initiated"
        elif value == "status":
            return status.main()
        elif value == "":
            return ""
    return "Unknown command "+ string
