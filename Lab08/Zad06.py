import sys
import socket
from enum import Enum
import json
import functools
import traceback


HOST = "127.0.0.1"
PORT = 5556

CRLF = "\r\n"

FOLDER_DELIMITER = "/"


class IMAPResponseStatus(Enum):
    OK = "OK"
    NO = "NO"
    BAD = "BAD"


class IMAPMessageFlag(Enum):
    SEEN = "\Seen"
    ANSWERED = "\Answered"
    FLAGGED = "\Flagged"
    DELETED = "\Deleted"
    DRAFT = "\Draft"
    RECENT = "\Recent"


class IMAPCommandType(Enum):
    NOOP = "NOOP" # +
    LOGOUT = "LOGOUT"
    # STARTTLS = "STARTTLS"
    # AUTHENTICATE = "AUTHENTICATE"
    LOGIN = "LOGIN" # +
    SELECT = "SELECT" # +
    CREATE = "CREATE" # +
    DELETE = "DELETE" # +
    RENAME = "RENAME" # +
    LIST = "LIST" # +
    STATUS = "STATUS" # +
    CLOSE = "CLOSE" # +
    EXPUNGE = "EXPUNGE" # +
    SEARCH = "SEARCH" # +
    FETCH = "FETCH"
    STORE = "STORE"


class IMAPSearchParameters(Enum):
    ALL = "ALL"
    NEW = "NEW"
    BODY = "BODY"
    FROM = "FROM"
    

class IMAPStatusDataItem(Enum):
    MESSAGES = "MESSAGES"
    RECENT = "RECENT"
    UIDNEXT = "UIDNEXT"
    UIDVALIDITY = "UIDVALIDITY"
    UNSEEN = "UNSEEN"


class IMAPServerState(Enum):
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    AUTHENTICATED = "AUTHENTICATED"
    SELECTED = "SELECTED"


class IMAPErrorMessage(Enum):
    INVALID_COMMAND = "Invalid command"
    INVALID_STATE = "Invalid state"
    INVALID_ARGUMENTS = "Invalid arguments"
    INVALID_USERNAME = "Invalid username"
    INVALID_PASSWORD = "Invalid password"
    INVALID_MESSAGE_NUMBER = "Invalid message number"
    NO_SUCH_MAILBOX = "No such mailbox"
    MAILBOX_NO_SELECT = "Mailbox cannot be selected"
    CANNOT_DELETE_TOP_MAILBOX = "Cannot delete top-level mailbox"
    MAILBOX_EXISTS = "Mailbox already exists"
    INVALID_STATUS_DATA_ITEM = "Invalid status data item"
    INVALID_SEARCH_PARAMETERS = "Invalid search parameters"


class IMAPResponse:
    def __init__(self, message: str, isLogout: bool = False):
        self.message = message
        self.isLogout = isLogout


class IMAPServer:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        self.user = None
        self.selected_folder = None
        self.read_db()
        self.state = IMAPServerState.NOT_AUTHENTICATED


    def read_db(self):
        with open('db.json', 'r') as f:
            self.db = json.load(f)


    def __del__(self):
        self.socket.close()


    def start_server(self):
        print("Strarting server...")
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Listening on port', self.port)
        while True:
            try:
                connection, address = self.socket.accept()
                print('Connected by', address)
                self.handle_connection(connection)
                connection.close()
                print('Connection closed')
            except Exception as e:
                print("An exception occurred:", e)
                tb = traceback.format_exc()
                print(tb)

                if connection:
                    connection.close()
            
            self.username = None
            self.password = None
            self.user = None
            self.selected_folder = None
            self.state = IMAPServerState.NOT_AUTHENTICATED


    def handle_connection(self, connection: socket.socket):
        connection.sendall(bytes(" ".join(["*", IMAPResponseStatus.OK.value, "Supported commands: [" + " ".join([cmd.value for cmd in IMAPCommandType]) + "]. Server ready.", CRLF]), 'utf-8'))
        while True:
            request = connection.recv(1024)
            if not request:
                break
            response = self.handle_request(request.decode('utf-8'))
            connection.sendall(bytes(response.message, 'utf-8'))

            if response.isLogout:
                break

    
    def handle_request(self, request: str) -> IMAPResponse:
        print("Recieved request:", request)
        request = request.replace(CRLF, '')
        request = request.split(' ')

        if len(request) < 2:
            return self.handle_invalid_arguments()
        

        match request[1].upper():
            case IMAPCommandType.NOOP.value:
                return self.handle_noop(request)
            case IMAPCommandType.LOGOUT.value:
                return self.handle_logout(request)
            case IMAPCommandType.LOGIN.value:
                return self.handle_login(request)
            case IMAPCommandType.SELECT.value:
                return self.handle_select(request)
            case IMAPCommandType.CREATE.value:
                return self.handle_create(request)
            case IMAPCommandType.DELETE.value:
                return self.handle_delete(request)
            case IMAPCommandType.RENAME.value:
                return self.handle_rename(request)
            case IMAPCommandType.LIST.value:
                return self.handle_list(request)
            case IMAPCommandType.STATUS.value:
                return self.handle_status(request)
            case IMAPCommandType.CLOSE.value:
                return self.handle_close(request)
            case IMAPCommandType.EXPUNGE.value:
                return self.handle_expunge(request)
            case IMAPCommandType.SEARCH.value:
                return self.handle_search(request)
        
        return self.handle_invalid_command(request)
    

    def handle_noop(self, request: list[str]) -> IMAPResponse:
        return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="NOOP completed")
    

    def handle_logout(self, request: list[str]) -> IMAPResponse:
        return self.handle_response(IMAPResponseStatus.OK, lines=["BYE IMAP4rev1 Server logging out"], tag=request[0], comment="Logout completed", isLogout=True)
    

    def handle_login(self, request: list[str]) -> IMAPResponse:
        if self.state != IMAPServerState.NOT_AUTHENTICATED:
            return self.handle_invalid_state(request)
        
        if len(request) < 4:
            return self.handle_invalid_arguments()
        
        username = request[2]
        password = request[3]

        try:
            userIdx = list(map(lambda user: user["username"], self.db["users"])).index(username)
            user = self.db["users"][userIdx]

            if user["password"] != password:
                return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.INVALID_PASSWORD.value, tag=request[0])
        
            self.state = IMAPServerState.AUTHENTICATED
            self.username = username
            self.password = password
            self.user = user

            return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="LOGIN completed")
        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.INVALID_USERNAME.value, tag=request[0])


    def handle_select(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 3:
            return self.handle_invalid_arguments()
        
        mailbox = request[2]

        folders = mailbox.split(FOLDER_DELIMITER)
        current_folder = self.user

        try:
            for folder in folders:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]
            
            if current_folder["isNoSelect"]:
                return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.MAILBOX_NO_SELECT.value, tag=request[0])

            self.state = IMAPServerState.SELECTED
            self.selected_folder = current_folder

            flagsMsg = "FLAGS (" + " ".join([flag.value for flag in IMAPMessageFlag]) + ")"
            existsMsg = str(len(current_folder["messages"])) + " EXISTS"
            recentMsg = str(len(list(filter(lambda msg: self.check_if_has_flag(msg, IMAPMessageFlag.RECENT), current_folder["messages"])))) + " RECENT"
            

            return self.handle_response(IMAPResponseStatus.OK, lines=[flagsMsg, existsMsg, recentMsg], tag=request[0], comment="[READ-WRITE] SELECT completed")
        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value, tag=request[0])
        
    
    def handle_create(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 3:
            return self.handle_invalid_arguments()
        
        mailbox = request[2]

        folders = mailbox.split(FOLDER_DELIMITER)
        current_folder = self.user

        try:
            for folder in folders:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]

            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.MAILBOX_EXISTS.value, tag=request[0])
        except ValueError:
            pass

        current_folder = self.user

        for folder in folders:
            try:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]
            except ValueError:
                current_folder["topMailboxID"] += 1
                current_folder["folders"].append({
                                "id": current_folder["topMailboxID"],
                                "topMailboxID": 0,
                                "topMessageID": 0,
                                "name": folder,
                                "isNoSelect": False,
                                "messages": [],
                                "folders": []
                            })
                current_folder = current_folder["folders"][-1]

        
        return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="CREATE completed")
        
    
    def handle_delete(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 3:
            return self.handle_invalid_arguments()
        
        mailbox = request[2]

        folders = mailbox.split(FOLDER_DELIMITER)

        if len(folders) < 2:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.CANNOT_DELETE_TOP_MAILBOX.value, tag=request[0])

        current_folder = self.user

        try:
            for folder in folders:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]
            
            if current_folder["isNoSelect"]:
                return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.MAILBOX_NO_SELECT.value, tag=request[0])
            
            if len(current_folder["folders"]) > 0:
                current_folder["isNoSelect"] = True
                current_folder["messages"] = []

                return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="DELETE completed")


            current_folder = self.user

            for folder in folders[:-1]:
                parent_folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][parent_folder_idx]

            current_folder["folders"].pop(folder_idx)

            return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="DELETE completed")
        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value, tag=request[0])

    
    def handle_rename(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 4:
            return self.handle_invalid_arguments()
        
        old_mailbox = request[2]
        new_mailbox = request[3]

        folders = old_mailbox.split(FOLDER_DELIMITER)

        current_folder = self.user

        try:
            for folder in folders:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]
            
            current_folder["name"] = new_mailbox
            return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="RENAME completed")

        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value, tag=request[0])


    def handle_list(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 4:
            return self.handle_invalid_arguments()
        
        reference = request[2]
        mailbox = request[3]

        if reference != "\"\"":
            referenceFolders = reference.split(FOLDER_DELIMITER)
        else:
            referenceFolders = []

        current_folder = self.user

        try:
            if len(referenceFolders) > 0:
                for folder in referenceFolders:
                    folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                    current_folder = current_folder["folders"][folder_idx]
                
            if mailbox == "\"\"":
                return self.handle_response(IMAPResponseStatus.OK, lines=["LIST " + "\"" + FOLDER_DELIMITER + "\" " + "\"\""], tag=request[0], comment="LIST completed")
            
            folders = mailbox.split(FOLDER_DELIMITER)

            try:
                for folder in folders[:-1]:
                    folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                    current_folder = current_folder["folders"][folder_idx]
            except ValueError:
                return self.handle_response(IMAPResponseStatus.NO, tag=request[0], comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value)
            
            lines = []

            if folders[-1] == "%":
                for folder in current_folder["folders"]:
                    lines.append("LIST " + ("(\\Noselect)" if folder["isNoSelect"] else "") + " " + folder["name"])
            elif folders[-1] == "*":
                lines = self.get_folders_in_mailbox(current_folder)  

            return self.handle_response(IMAPResponseStatus.OK, lines=lines, tag=request[0], comment="LIST completed")

        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value, tag=request[0])

    
    def get_folders_in_mailbox(self, mailbox, prefix: str="") -> list[str]:
        folders = []

        for folder in mailbox["folders"]:
            folders.append("LIST " + ("(\\Noselect)" if folder["isNoSelect"] else "") + " " + prefix + folder["name"])

            folders.extend(self.get_folders_in_mailbox(folder, prefix + folder["name"] + FOLDER_DELIMITER))
        
        return folders
    

    def handle_status(self, request: list[str]) -> IMAPResponse:
        if self.state not in [IMAPServerState.AUTHENTICATED, IMAPServerState.SELECTED]:
            return self.handle_invalid_state(request)
        
        if len(request) < 4:
            return self.handle_invalid_arguments()
        
        mailbox = request[2]
        status_data_items = request[3:]
        status_data_items[0] = status_data_items[0][1:]
        status_data_items[-1] = status_data_items[-1][:-1]

        folders = mailbox.split(FOLDER_DELIMITER)

        current_folder = self.user

        try:
            for folder in folders:
                folder_idx = list(map(lambda f: f["name"].upper(), current_folder["folders"])).index(folder.upper())
                current_folder = current_folder["folders"][folder_idx]
            
            status = []

            for status_data_item in status_data_items:
                if status_data_item.upper() == IMAPStatusDataItem.MESSAGES.value:
                    status.append(IMAPStatusDataItem.MESSAGES.value + " " + str(len(current_folder["messages"])))
                elif status_data_item.upper() == IMAPStatusDataItem.RECENT.value:
                    status.append(IMAPStatusDataItem.RECENT.value + " " + str(len(list(filter(lambda m: self.check_if_has_flag(m, IMAPMessageFlag.RECENT), current_folder["messages"])))))
                elif status_data_item.upper() == IMAPStatusDataItem.UIDNEXT.value:
                    status.append(IMAPStatusDataItem.UIDNEXT.value + " " + str(current_folder["topMailboxID"] + 1))
                elif status_data_item.upper() == IMAPStatusDataItem.UIDVALIDITY.value:
                    status.append(IMAPStatusDataItem.UIDVALIDITY.value + " " + str(0))
                elif status_data_item.upper() == IMAPStatusDataItem.UNSEEN.value:
                    status.append(IMAPStatusDataItem.UNSEEN.value + " " + str(len(list(filter(lambda m: not self.check_if_has_flag(m, IMAPMessageFlag.SEEN), current_folder["messages"])))))
                else:
                    return self.handle_response(IMAPResponseStatus.BAD, comment=IMAPErrorMessage.INVALID_STATUS_DATA_ITEM.value, tag=request[0])
            
            statusStr = "STATUS " + mailbox + " (" + " ".join(status) + ")"

            return self.handle_response(IMAPResponseStatus.OK, lines=[statusStr], tag=request[0], comment="STATUS completed")

        except ValueError:
            return self.handle_response(IMAPResponseStatus.NO, comment=IMAPErrorMessage.NO_SUCH_MAILBOX.value, tag=request[0])


    def handle_close(self, request: list[str]) -> IMAPResponse:
        if self.state != IMAPServerState.SELECTED:
            return self.handle_invalid_state(request)
        
        self.selected_folder["messages"] = list(filter(lambda m: not self.check_if_has_flag(m, IMAPMessageFlag.DELETED), self.selected_folder["messages"]))
        
        self.state = IMAPServerState.AUTHENTICATED
        self.selected_folder = None

        return self.handle_response(IMAPResponseStatus.OK, tag=request[0], comment="CLOSE completed")


    def handle_expunge(self, request: list[str]) -> IMAPResponse:
        if self.state != IMAPServerState.SELECTED:
            return self.handle_invalid_state(request)
        
        deleted_messages = list(filter(lambda m: self.check_if_has_flag(m, IMAPMessageFlag.DELETED), self.selected_folder["messages"]))
        
        self.selected_folder["messages"] = list(filter(lambda m: m not in deleted_messages, self.selected_folder["messages"]))
        deleted_messages_lines = list(map(lambda m: str(m["uid"]) + " EXPUNGE", deleted_messages))

        return self.handle_response(IMAPResponseStatus.OK, lines=deleted_messages_lines, tag=request[0], comment="EXPUNGE completed")


    def handle_search(self, request: list[str]) -> IMAPResponse:
        if self.state != IMAPServerState.SELECTED:
            return self.handle_invalid_state(request)
        
        if len(request) < 3:
            return self.handle_invalid_arguments()
        
        search_criteria = request[2:]
        search_criteria[0] = search_criteria[0][1:]
        search_criteria[-1] = search_criteria[-1][:-1]

        search_results = self.selected_folder["messages"]
        
        idx = 0
        while idx < len(search_criteria):
            if search_criteria[idx].upper() == IMAPSearchParameters.ALL.value:
                idx += 1
            elif search_criteria[idx].upper() == IMAPSearchParameters.NEW.value:
                search_results = list(filter(lambda m: self.check_if_has_flag(m, IMAPMessageFlag.RECENT), search_results))
                idx += 1
            elif search_criteria[idx].upper() == IMAPSearchParameters.BODY.value:
                search_results = list(filter(lambda m: search_criteria[idx + 1] in m["body"], search_results))
                idx += 2
            elif search_criteria[idx].upper() == IMAPSearchParameters.FROM.value:
                search_results = list(filter(lambda m: search_criteria[idx + 1] == m["from"], search_results))
                idx += 2
            else:
                return self.handle_response(IMAPResponseStatus.BAD, comment=IMAPErrorMessage.INVALID_SEARCH_PARAMETERS.value, tag=request[0])
        
        search_results_lines = list(map(lambda m: str(m["uid"]), search_results))
        search_results_lines_str = "SEARCH " + " ".join(search_results_lines)
        return self.handle_response(IMAPResponseStatus.OK, lines=[search_results_lines_str], tag=request[0], comment="SEARCH completed")
        

    def check_if_has_flag(self, message, flag: IMAPMessageFlag) -> bool:
        return flag.value in message["flags"]


    def handle_invalid_command(self, request: list[str]) -> IMAPResponse:
        return self.handle_response(IMAPResponseStatus.BAD, tag=request[0], comment=IMAPErrorMessage.INVALID_COMMAND.value)
    

    def handle_invalid_state(self, request: list[str]) -> IMAPResponse:
        return self.handle_response(IMAPResponseStatus.BAD, comment=IMAPErrorMessage.INVALID_STATE.value, tag=request[0])
    

    def handle_invalid_arguments(self) -> IMAPResponse:
        return self.handle_response(IMAPResponseStatus.BAD, comment=IMAPErrorMessage.INVALID_ARGUMENTS.value)
        

    def handle_response(self, response_status: IMAPResponseStatus, lines: list[str] = [], tag: str = "*", comment: str = "", isLogout: bool = False) -> IMAPResponse:
        if lines:
            linesStr = CRLF.join(["* " + line for line in lines]) + CRLF + tag
            return IMAPResponse(" ".join([linesStr, response_status.value, comment, CRLF]), isLogout)
        
        return IMAPResponse(" ".join([tag, response_status.value, comment, CRLF]), isLogout)


if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server = IMAPServer(HOST, port)
    server.start_server()