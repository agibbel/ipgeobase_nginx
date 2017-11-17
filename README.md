# Импорт геоданных из IpGeoBase в Nginx
База [IpGeoBase](http://ipgeobase.ru/) предоставляет наиболее полные данные по географическому местонахождению IP-адреса, выделенного RIPE локальным интернет-реестрам (LIR-ам) для Российской Федерации и Украины. Для использования необходим [nginx_geo_module](http://nginx.org/ru/docs/http/ngx_http_geo_module.html).
## Установка
1. Скачать файл
2. Прописать запуск в Cron
3. Подключить файл geo в конфигурации Nginx
4. Использовать переменные $country, $region, $city, $latitude, $longitude
