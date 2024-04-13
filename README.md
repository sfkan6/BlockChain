# Простой Блокчейн


Учебный проект для знакомства с принципом работы блокчейна. 

<br>
<hr>
<br>

## Установка: 

### Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone https://github.com/sfkan6/BlockChain.git
```
```sh
cd BlockChain
```

### Запуск:

1. Cоздать и активировать виртуальное окружение:
```sh
python -m venv venv
```

```sh
source venv/Scripts/activate
```
или
```sh
source venv/bin/activate
```

2. Установите зависимости:
```sh
pip install -r requirements.txt
```

3. Запустите:
```sh
uvicorn main:app
```

### Docker:
```sh
docker build -t blockchain .
```
```sh
docker run --rm -p 8000:8000 -it blockchain
```
