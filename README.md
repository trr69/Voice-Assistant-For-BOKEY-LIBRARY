# VoiceAssistant

![VoiceAssistant](./img/woman.jpg)

Это голосовой ассистент магнус с возможностью RAG. Ассистент требует python версии 3.11.7

![Mind Map](./img/schema.png)
*Mind Map for the Voice Assistant (deprecated)*

## Table of Contents

- [Установка](#installation)
- [Использование](#usage)
- [Contributing](#contributing)

## Installation

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/trr69/Voice-Assistant-For-BOKEY-LIBRARY.git
    ```

2. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```
8. **Download Vosk model:**

    Установите модель воск [здесь](https://alphacephei.com/vosk/models).

5. **Настройте файл config.py:**

    Скопируйте openai api и путь до vosk model, и вставьте в config.py

6 **Добавьте ваши данные в data/books**

7 **Создание векторной базы данных**

    Выполните create_database.py для создания векторной базы данных в "chroma/chroma.sqlite3"

## Usage

Запустите голосового ассистента и пользуйтесь

```bash
python main.py
```


## Contributing
