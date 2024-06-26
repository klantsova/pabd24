# Отчет по семинару № 3
Исследование поведения серверов flask и gunicorn под разными видами нагрузки.  
**Выполнила:** Ланцова Ксения

### Введение
Для тяжелых моделей предиктивной аналитики возможно два варианта деплоя. 
Первый вариант - запускать модели на своем сервере. 
Этот вариант имеет очевидный недостаток. 
Если у вас очень тяжелая модель, то пользователи вашего сервиса должны будут долго ждать ответа.  
Даже самый мощный компьютер имеет предел вычислительной мощности. 
Поэтому если вашим сервисом будут пользоваться несколько пользователей одновременно, придется настраивать собственный вычислительный кластер. 

Второй вариант - использовать специальные сервисы, например:  
- TensorFlow Serving
- AWS SageMaker
- Yandex DataSphere
- Google Vertex AI

В этом случае вычислительная нагрузка снимается с вашего сервера. 
Но за каждый запрос к стороннему сервису нужно платить, как деньги, так и временем на обработку запросов. 

### Метод исследования
В файле `src/utils.py` определены три функции, которые эмулируют три варианта решения задачи `predict` :
- `predict_io_bounded(area)` - соответсвует второму варианту, запрос к стороннему сервису заменяет `time.sleep(1)`. 
Это соответствует задержке в 1 секунду, которая нужна для обмена информацией со сторонним сервисом. 
При этом вычислительная нагрузка на наш сервер не создается, процесс просто спит. 
- `predict_cpu_bounded(area, n)` - соответствует первому варианту, предикту на собственном сервере. 
Параметр `n` позволяет регулировать нагрузку, на самом деле это просто вычисление среднего арифметического линейного массива. 
При достаточно больших `n` сервер будет выдавать ошибку из-за нехватки памяти. 
Необходимо эмпирическим путем определить это значение. 
- `predict_cpu_multithread(area, n)` - тоже соответствует первому варианту, но используется оптимизированный код на numpy. 
Необходимо также эмпирическим путем определить критическое значение `n` и сравнить его с предыдущим. 

Для запуска сервиса доступно два варианта: 
- `python src/predict_app.py` - сервер, предназначенный для разработки. 
- `gunicorn src.predict_app:app` - сервер, предназначенный для непрерывной работы в продакшн. 

Нагрузка создается файлом `test/test_parallel.py`.  

**Задача**: запустить 6 (шесть) возможных вариантов сочетаний серверов и функций под нагрузкой в 10 запросов. 

### Результат и обсуждение
*Значения n перебирались интервалом по 5 миллионов.*
1) При запуске **predict_io_bounded** на dev-сервере flask получен [результат](../log/test_pib_flask.txt). 
Все запросы обрабатываются одновременно, в среднем за 11 секунд. На продакшене это неприемлимо, потому что при большом кол-ве запросов нужно распределять нагрузку на сервер.
2) При запуске **predict_io_bounded** на prod-сервере gunicorn получен [результат](../log/test_pib_gunicorn.txt). 
Все запросы обрабатываются последовательно, в среднем за 56 секунд. Все запросы обрабатываются по очереди. На продакшене это предпочтительнее, потому что при таком распределении разгрузки сервер работает лучше и стабильнее.
3) При запуске **predict_cpu_bounded** с n = 10_000_000 (это максимальное подобранное значение n, при котором нет ошибки) на dev-сервере flask получен [результат](../log/test_pcb_flask_10m.txt). 
Все запросы обрабатываются одновременно, в среднем за 47 секунд. Для более стабильной работы сервера стоит распределять нагрузку.
4) При запуске **predict_cpu_bounded** с n = 85_000_000 (это максимальное подобранное значение n, при котором нет ошибки) на prod-сервере gunicorn получен [результат](../log/test_pcb_gunicorn_85m.txt). 
Все запросы обрабатываются последовательно, в среднем за 4.5 минуты. Видно, что на prod-сервере удастся увеличить n в 8.5 раз, что связано с упорядочиванием запросов.
5) При запуске **predict_cpu_multithread** с n = 40_000_000 (это максимальное подобранное значение n, при котором нет ошибки) на dev-сервере flask получен [результат](../log/test_pcm_flask_40m.txt). 
Все запросы обрабатываются одновременно, в среднем за 7 секунд. Видим, что результат значительно быстрее предыдущего метода, так как используется встроенная библиотека numpy.
6) При запуске **predict_cpu_multithread** с n = 435_000_000 (это максимальное подобранное значение n, при котором нет ошибки) на prod-сервере gunicorn получен [результат](../log/test_pcm_gunicorn_435m.txt). 
Все запросы обрабатываются последовательно, в среднем за 1.7 минут. Видим, что результат значительно быстрее предыдущего метода (при большем n), так как используется встроенная библиотека numpy.

 


