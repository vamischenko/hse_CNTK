# hse_CNTK

### Language understanding (CNTK). Применение библиотеки Microsoft CNTK для построения нейросетевых моделей текстов.

##### Состав команды:
Кузнецов Владимир

Вороная Ксения

Куренков Евгений

##### -----------------------------------------------------------------------------

##### Цель нашей работы: Language Understanding with Recurrent Networks


##### План работы:
Первичное изучение библиотеки

 https://github.com/Microsoft/CNTK/wiki
 
https://www.microsoft.com/en-us/research/publication/an-introduction-to-computational-networks-and-the-computational-network-toolkit/

Установка и настройка 

Обучение моделей, запуск и разбор готовых примеров: 

ATIS https://github.com/Microsoft/CNTK/tree/master/Examples/Text/ATIS

PennTreebank

Написание собственной утилиты

##### -----------------------------------------------------------------------------


##### Установка (2 пути):

####### Через бинарники на Linux 64bit и Windows (были добавлены в августе 2016)

https://github.com/Microsoft/CNTK/releases

для Windows:

Visual C++ Redistributable Package for Visual Studio 2013

Microsoft MPI of version 7 (7.0.12437.6)


для Linux

C++ Compiler

Open MPI 


For GPU systems latest NVIDIA driver.


####### Через Docker Containers
https://www.docker.com/products/docker-toolbox

Загрузить необходимые докер-файлы здесь https://github.com/Microsoft/CNTK/tree/master/Tools/docker

Сбилдить контейнер: 

docker build -t cntk CNTK-CPUOnly-Image

где cntk имя нашего образа 



Готовый образ можно взять здесь:

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
