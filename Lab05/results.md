# Wnioski 

##  Dla którego z gniazd czas jest krótszy?
Średni czas przesłania pakietu jest znacznie krótszy w przypadku połączenia UDP. 
W porównaniu z gniazdem TCP średni czas wysłania pakietu jest krótszy niemalże o połowę (czas przesyłania sekwencyjnie 100_000 pakietów wyniósł dla protokołów UDP I TCP odpowiednio 1.34s oraz 2.43s 

## Z czego wynika krótszy czas?
Krótszy czas przesyłania wynika z faktu iż protokół TCP wymaga potwierdzenia otrzymania kompletnego pakietu, a więc klient oczekuje na odpowiedź od serwera o poprawnym transferze. Z kolei protokół UDP nie wymaga żadnego potwierdzenia, dzięki czemu pakiety przesyłane są szybciej, jednak w związku z tym nie mamy pewności czy dotarły one do adresata. Dodatkowo pakiety TCP mają większy narzut danych (obszerniejsze nagłówki) co również obniża efektywnośc tego protokołu. 

 
## Jakie są zalety / wady obu rozwiązań?
### Zalety TCP: 
- Pewność dostarczenia pakietu – otrzymujemy informację dającą gwarancję, że pakiet dotarł do adresata 
- Weryfikacja kompletności wiadomości - w przypadku dostarczenia tylko części wiadomości lub wystąpienia błędów brakujące pakiety mogą zostać przesłane ponownie 
- Możliwość dostosowania tempa przesyłu od możliwości odbiorcy 

### Wady TCP 
- Wykorzystuje więcej transferu i jest wolniejsze od UDP - duży narzut, konieczność przesłania potwierdzeń odbioru 
- Nie posiada możliwości multicastu oraz broadcastu 
- Nie pozwala na wczytanie zasobu do momentu jego kompletnego przesłania 

### Zalety UDP 
- Nie wymaga utrzymywania połączenia 
- Nie wymaga potwierdzenia dostarczenia, dzięki czemu transfer jest znacznie szybszy (niż w przypadku TCP) 
- Umożliwia broadcasting oraz multicasting pakietów 
- Dostarcza wiadomośc nawet w przypadku utracenia części danych 
- Jest bardziej efektywny od TCP 
- Umożliwia przesyłanie danych czasu rzeczywistego (streaming, wideorozmowy) 

### Wady UDP 
- Przesył danych nie jest niezawodny – istnieje możliwość utraty części informacji 
- Brak potwierdzenia otrzymania pakietów 
- Ryzyko dostarczenia niepełnych lub uszkodzonych danych 
- Brak możliwości reagowania na błędy 
- Nie ma pewności, że dane będą dostarczone w odpowiedniej kolejności. 