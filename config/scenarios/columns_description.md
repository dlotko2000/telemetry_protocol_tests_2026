## Experimental Results Column Descriptions

###### Raw Data (raw_results.csv)

- scenario_id – scenario identifier
- protocol – communication protocol
- run_number – run number
- message_id – message identifier
- send_timestamp – send time
- receive_timestamp – receive time
- latency_ms – RTT latency
- status – operation status
- payload_size – data size
- response_size – response size
- http_status_code – HTTP code
- error_message – error description

###### Aggregated Data (summary.csv)

- success_rate – transmission efficiency
- throughput_msg_s – throughput
- avg_latency_ms – average latency
- avg_cpu_percent_process – average CPU
- avg_memory_rss_mb – average RAM
- total_net_bytes_sent – ​​data sent
- total_net_bytes_recv – received data

# Polish descripton:

## Opis kolumn wyników eksperymentalnych

###### Dane surowe (raw_results.csv)

- scenario_id – identyfikator scenariusza
- protocol – protokół komunikacyjny
- run_number – numer przebiegu
- message_id – identyfikator wiadomości
- send_timestamp – czas wysłania
- receive_timestamp – czas odebrania
- latency_ms – opóźnienie RTT
- status – status operacji
- payload_size – rozmiar danych
- response_size – rozmiar odpowiedzi
- http_status_code – kod HTTP
- error_message – opis błędu

###### Dane zagregowane (summary.csv)

- success_rate – skuteczność transmisji
- throughput_msg_s – przepustowość
- avg_latency_ms – średnie opóźnienie
- avg_cpu_percent_process – średnie CPU
- avg_memory_rss_mb – średni RAM
- total_net_bytes_sent – wysłane dane
- total_net_bytes_recv – odebrane dane