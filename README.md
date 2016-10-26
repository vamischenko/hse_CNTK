## Language understanding (CNTK). Применение библиотеки Microsoft CNTK для построения нейросетевых моделей текстов.

Ссылка на библиотеку: https://github.com/Microsoft/CNTK/tree/master/

CNTK_LICENSE.md - лицензия по использованию 

### Состав команды:
Кузнецов Владимир

Вороная Ксения

Куренков Евгений

##### -----------------------------------------------------------------------------

### Цель нашей работы: Language Understanding with Recurrent Networks LSTM, 
хотим понять о чем human query, и в итоге проставить предложению-запросу определенный лейбл-тег


### Ход работы:

##### Первичное изучение библиотеки по следующим ресурсам:

https://github.com/Microsoft/CNTK/wiki
 
https://www.microsoft.com/en-us/research/publication/an-introduction-to-computational-networks-and-the-computational-network-toolkit/

Смотрите также презентацию проекта - CNTK_language_understanding.pdf

##### Установка и настройка 

необходимая информация приведена ниже

##### Обучение моделей, запуск и разбор готовых примеров: 

ATIS https://github.com/Microsoft/CNTK/tree/master/Examples/Text/ATIS

PennTreebank

В презентации приведены результаты работы примеров

##### Написание собственной утилиты

В каталоге Python содержится разработанное консольное приложение, использующее натренированную рекурентную LSTM.

ATIS.py - сам скрипт приложения

SLUHands.cntk и pyConfig.cntk - конфиги для запуска

atis.train.ctf и atis.test.ctf - данные для обучения и проверки работы сети

##### -----------------------------------------------------------------------------


### Установка CNTK(2 пути):

##### Через бинарники на Linux 64bit и Windows (были добавлены в августе 2016)

Качаем бинарники здесь: https://github.com/Microsoft/CNTK/releases


для Windows потребуется:

Visual C++ Redistributable Package for Visual Studio 2013

Microsoft MPI of version 7 (7.0.12437.6)


для Linux потребуется:

C++ Compiler

Open MPI 


For GPU systems latest NVIDIA driver.

В рамках данного проекта мы работали только с CPU.


##### Через Docker Containers

Качаем toolbox здесь: https://www.docker.com/products/docker-toolbox

Загрузить необходимые докер-файлы здесь https://github.com/Microsoft/CNTK/tree/master/Tools/docker

Зайти в Docker Quickstart Terminal.


Сбилдить контейнер: 

docker build -t cntk CNTK-CPUOnly-Image

где cntk имя нашего образа 

Контейнер билдится достаточно долго...


Поэтому готовый образ можно взять здесь:

https://hub.docker.com/r/torumakabe/cntk-cpu/

docker pull torumakabe/cntk-cpu


Запустить образ а затем пример: 

docker run –it –-rm cntk

cd Examples/Text/PennTreebank/Data

cntk configFile=../Config/rnn.cntk


##### -----------------------------------------------------------------------------


##### Цель: создать и обучить рекуррентную нейронную сеть для задач тегирования и классификации данных от Аir Travel Information Services (ATIS). 
Тasks of slot tagging and intent classification.

##### Необходимое:

Recurrent neural network

Word embedding (векторное представление слов)


##### Запуск примера:
cd Examples/Text/ATIS
cntk configFile=ATIS.cntk

##### -----------------------------------------------------------------------------

### Как запустить приложение:

Смотри README файл в каталоге Python.