import socket, ssl, time, sys, random, json

HOST = "chat.freenode.net"
PORT = 7000
NICK = "ircBot"
NAME = "ircBotName"
CHANNEL = "#test123"

WEATHER_API_KEY = "d4af3e33095b8c43f1a6815954face64"
WEATHER_API_HOST = "api.openweathermap.org"
WEATHER_API_PORT = 443


class WeatherCLient:
    def __init__(self, host=WEATHER_API_HOST, port=WEATHER_API_PORT, key=WEATHER_API_KEY):
        self.host = host
        self.port = port
        self.key = key
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.secure_sock = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLSv1_2)

    def __del__(self):
        self.secure_sock.close()
        self.sock.close()
        

    def getWeather(self, city):
        self.secure_sock.sendall(("GET /data/2.5/weather?q=" + city + "&appid=" + self.key + "\r\n").encode())
        recieved = self.secure_sock.recv(4096)
        print("Received from weather api: ", recieved)
        return self.format_response(recieved.decode())
    
    def format_response(self, response):
        res = json.loads(response)
        coords = res["coord"]
        weather = res["weather"][0]
        main = res["main"]
        wind = res["wind"]
        clouds = res["clouds"]
        sys = res["sys"]

        weatherResponse = "Coordinates: " + str(coords["lon"]) + ", " + str(coords["lat"]) + " | "
        weatherResponse += "Description: " + weather["main"] + " - " + weather["description"] + " | "
        weatherResponse += "Temperature: " + str(round(main["temp"] - 273, 2)) + "C | "
        weatherResponse += "Pressure: " + str(main["pressure"]) + "hPa | "
        weatherResponse += "Humidity: " + str(main["humidity"]) + "% | "
        weatherResponse += "Wind: " + str(wind["speed"]) + "m/s | "
        weatherResponse += "Clouds: " + str(clouds["all"]) + "% | "
        weatherResponse += "Sunrise: " + time.ctime(sys["sunrise"]) + " | "
        weatherResponse += "Sunset: " + time.ctime(sys["sunset"])
    
        return weatherResponse


class IRCClient:
    def __init__(self, host=HOST, port=PORT, nick=NICK, name=NAME, channel=CHANNEL):
        randomNick = nick + str(random.randint(0, 1000))

        self.host = host
        self.port = port
        self.nick = randomNick
        self.name = name
        self.channel = channel
        self.weatherCLient = WeatherCLient()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def setupVerifiedConnection(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_default_certs()

        if ssl.HAS_SNI:
            self.secure_sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
        else:
            self.secure_sock = self.context.wrap_socket(self.sock)
        
        cert = self.secure_sock.getpeercert()

        if not cert or ssl.match_hostname(cert, self.host):
            raise Exception("Invalid SSL certificate")
        
    def getWeather(self, city):
        return self.weatherCLient.getWeather(city)
        
    def send(self, message):
        print("Sending: ", message)
        self.secure_sock.send(message.encode())

    def sendall(self, message):
        print("Sending: ", message)
        self.secure_sock.sendall(message.encode())

    def recv(self):
        received = self.secure_sock.recv().decode('utf-8')
        print("Received: ", received)
        return received
    
    def sendPrivateMessage(self, message):
        self.sendall("PRIVMSG " + self.channel + " :" + message + "\r\n")
    
    def initializeChat(self):
        self.sendall("NICK " + self.nick + "\r\n")
        self.sendall("USER " + self.nick + " 0 * :" + self.name + "\r\n")
        self.sendall("JOIN " + self.channel + "\r\n")

    def interpretMessage(self, message):
        if message == "!hello":
            self.sendPrivateMessage("Hello!")
        elif message == "!quit":
            self.sendall("QUIT\r\n")
        elif message == "!time":
            self.sendPrivateMessage(time.strftime("%H:%M:%S", time.localtime()))
        elif message == "!date":
            self.sendPrivateMessage(time.strftime("%d.%m.%Y", time.localtime()))
        elif message.startswith("!weather"):
            splitted = message.split(" ")
            if len(splitted) == 2:
                city = splitted[1]
                self.sendPrivateMessage("Weather in " + city.upper() + ": " + self.getWeather(city.lower()))
            else:
                self.sendPrivateMessage("Invalid command")
        elif message == "!help":
            self.sendPrivateMessage("Commands: !hello, !time, !date, !weather <city>, !quit")

    def run(self):
        while True:
            received = self.recv()
            if not received:
                break

            if "451" in received:
                self.sendall("JOIN " + self.channel + "\r\n")
            elif received.startswith("PING :"):
                ping = received.split("PING :")[1]
                self.sendall(("PONG " + ping + "\r\n"))
            elif ("PRIVMSG " + self.channel + " :") in received:
                message = received.split("PRIVMSG " + self.channel + " :")[1]
                print("Message: ", message)
                self.interpretMessage(message.strip("\r\n"))

        self.secure_sock.close()


if __name__ == "__main__":
    nick = NICK
    name = NAME
    channel = CHANNEL

    if len(sys.argv) == 4:
        nick = sys.argv[1]
        name = sys.argv[2]
        channel = sys.argv[3]

    client = IRCClient(HOST, PORT, nick, name, channel)
    client.setupVerifiedConnection()
    time.sleep(1)
    client.initializeChat()
    client.run()