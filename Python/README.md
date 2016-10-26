#Python

Это пример простого консольного приложения, использующего натренированную рекуррентную нейронную сеть LSTM из примера https://github.com/Microsoft/CNTK/tree/master/Examples/Tutorials/SLUHandsOn для понимания содержания предложения.

Обучение модели:

* CNTK.exe configFile=./SLUSentence.cntk
* CNTK.exe configFile=./SLUWord.cntk

Запуск скрипта:

* python ATIS.py
* Вводите любое предложение на английском языке (лучше про авиаперевозки).