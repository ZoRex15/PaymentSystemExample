<h1>PaymentSystem Example</h1>
<p>Простой пример сервиса, который может отвечать за работу с платежами в вашем проекте.</p>

<h2>Используемые технологии</h2>
<ul>
    <li>Python: 3.11.5</li>
    <li>NATS</li>
    <li>FastStream</li>
    <li>Dishka</li>
    <li>SQLAlchemy</li>
    <li>PostgreSQL</li>
    <li>Alembic</li>
    <li>Docker</li>
</ul>

<h2>Запуск</h2>
<b>Примечание:</b> Для запуска используется Docker.<br><br>

<ol>
    <li>Клонируйте репозиторий на свой компьютер, используя эту команду:</li>
    <pre><code>git clone https://github.com/ZoRex15/PaymentSystemExample.git</code></pre>
    <li>Создайте файл <code>.settings.yml</code> в папке <code>config_dist</code> по примеру <code>example_settings.yml</code>.</li>
    <li>Введите команду <code>docker compose up</code>.</li>
    <li>После запуска примените миграции к БД, используя команду:</li>
    <pre><code>alembic upgrade head</code></pre>
</ol>

<h2>Пример запросов к сервису используя NATS CLI</h2>

<ul>
    <li><b>Примечание 1:</b> Пример запросов показан на Windows в CMD.</li>
    <li><b>Примечание 2:</b> В запросах не используйте <code>counteragent_id</code>, который равен одному, так как этот пользователь зарезервирован системой как CASH_BOOK.</li>
</ul>

<h3>Запрос на пополнение баланса:</h3>
<pre><code>nats request payments.counteragent.balance.replenishment "{\"counteragent_id\": 2, \"amount\": 350}" -H "X-Idempotency-Key:f47ac10b-58cc-4372-a567-0e02b2c3d479"</code></pre>

<h3>Запрос который снимает деньги с баланса:</h3>
<pre><code>nats request payments.counteragent.balance.withdrawal "{\"counteragent_id\": 2, \"amount\": 50}" -H "X-Idempotency-Key:f47ac10b-58cc-4372-a567-0e02b2c3d472"</code></pre>

<h3>Запрос на просмотр баланса:</h3>
<pre><code>nats request payments.counteragent.balance "{\"counteragent_id\": 2}"</code></pre>

<h2>Структура проекта</h2>
<pre>
📁 PaymentSystemExample/
├── 📁 app/
│   ├── __main__.py
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   ├── 📁 interfaces/
│   │   │   ├── __init__.py
│   │   │   └── 📁 repository/
│   │   │       ├── __init__.py
│   │   │       ├── base.py
│   │   │       ├── posting.py
│   │   │       └── transaction_log.py
│   │   ├── 📁 models/
│   │   │   ├── __init__.py
│   │   │   ├── 📁 dto/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── posting.py
│   │   │   │   └── transaction_log.py
│   │   │   ├── 📁 enum/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── db.py
│   │   │   │   └── reply.py
│   │   │   └── 📁 messages/
│   │   │       ├── __init__.py
│   │   │       ├── incoming_messages.py
│   │   │       └── outgoing_messages.py
│   │   └── 📁 service/
│   │       ├── __init__.py
│   │       ├── payments.py
│   │       └── posting.py
│   └── 📁 infrastructure/
│       ├── __init__.py
│       ├── 📁 broker/
│       │   ├── __init__.py
│       │   ├── 📁 consumers/
│       │   │   ├── __init__.py
│       │   │   ├── payment.py
│       │   │   └── payment_info.py
│       │   └── 📁 middlewares/
│       │       ├── __init__.py
│       │       ├── check.py
│       │       └── logging.py
│       ├── 📁 config/
│       │   ├── __init__.py
│       │   ├── logging.py
│       │   ├── main.py
│       │   ├── 📁 models/
│       │   │   ├── __init__.py
│       │   │   └── models.py
│       │   └── 📁 service/
│       │       ├── __init__.py
│       │       └── parsers.py
│       ├── 📁 db/
│       │   ├── __init__.py
│       │   ├── holder.py
│       │   ├── 📁 migration/
│       │   │   ├── README
│       │   │   ├── env.py
│       │   │   ├── script.py.mako
│       │   │   └── 📁 versions/
│       │   │       ├── 0d59302e6c47_db.py
│       │   ├── 📁 models/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── posting.py
│       │   │   └── transaction_log.py
│       │   └── 📁 repository/
│       │       ├── __init__.py
│       │       ├── base.py
│       │       ├── posting.py
│       │       └── transaction_log.py
│       └── 📁 di/
│           ├── __init__.py
│           ├── config.py
│           ├── db.py
│           └── fast_stream.py
├── 📁 config_dist/
│   ├── .settings.yml
│   ├── example_settings.yml
│   └── logging.yml
├── 📁 nats_docker_data/
│   ├── 📁 config/
│   │   └── server.conf
│   └── 📁 data/
│       └── 📁 jetstream/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
</pre>

<h3>📁 app/</h3>
<p><strong>Это основная папка приложения.</strong></p>

<h4>📁 core/</h4>
<p><strong>Содержит ключевые компоненты и бизнес-логику.</strong></p>

<ul>
    <li>📁 <strong>interfaces/</strong>: Определяет контракты для взаимодействия между различными компонентами.</li>
    <li>📁 <strong>interfaces/repository/</strong>: Содержит интерфейсы для доступа к данным.
        <ul>
            <li><code>base.py</code>: Базовый интерфейс, от которого наследуются другие.</li>
            <li><code>posting.py</code>: Интерфейсы для операций с таблицей Posting.</li>
            <li><code>transaction_log.py</code>: Интерфейсы для операций с таблицей TransactionLog.</li>
        </ul>
    </li>
    <li>📁 <strong>models/</strong>: Содержит модели данных и их представления.</li>
    <li>📁 <strong>models/dto/</strong>: Содержит DTO для передачи данных.
        <ul>
            <li><code>posting.py</code>: DTO для таблицы Posting.</li>
            <li><code>transaction_log.py</code>: DTO для TransactionLog.</li>
        </ul>
    </li>
    <li>📁 <strong>models/enum/</strong>: Содержит перечисления.
        <ul>
            <li><code>db.py</code>: Перечисления, связанные с базой данных.</li>
            <li><code>reply.py</code>: Перечисления для ответов системы.</li>
        </ul>
    </li>
    <li>📁 <strong>service/</strong>: Содержит бизнес-логику и сервисы.
        <ul>
            <li><code>payments.py</code>: Логика обработки платежей.</li>
            <li><code>posting.py</code>: Логика обработки запросов, связанных с таблицей Posting.</li>
        </ul>
    </li>
</ul>

<h4>📁 infrastructure/</h4>
<p><strong>Содержит инфраструктурные компоненты, такие как конфигурация, БД и т. д.</strong></p>

<ul>
    <li>📁 <strong>broker/</strong>: Компоненты для работы с брокером сообщений.
        <ul>
            <li>📁 <strong>consumers/</strong>: Реализации потребителей сообщений.
                <ul>
                    <li><code>payment.py</code>: Обработка запросов, связанных с платежами.</li>
                    <li><code>payment_info.py</code>: Обработка запросов на получение информации о платежах.</li>
                </ul>
            </li>
            <li>📁 <strong>middlewares/</strong>: Промежуточные обработчики.
                <ul>
                    <li><code>check.py</code>: Проверка запроса на наличие параметра reply.</li>
                    <li><code>logging.py</code>: Логирование событий.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>📁 <strong>config/</strong>: Логика работы с конфигурационными файлами.
        <ul>
            <li><code>logging.py</code>: Настройка логирования.</li>
            <li><code>main.py</code>: Парсинг файла с настройками.</li>
        </ul>
    </li>
    <li>📁 <strong>db/</strong>: Компоненты для работы с базой данных.
        <ul>
            <li><code>holder.py</code>: Класс, который содержит все репозитории.</li>
            <li>📁 <strong>migration/</strong>: Миграции для БД.</li>
            <li>📁 <strong>models/</strong>: Модели таблиц для БД.</li>
            <li>📁 <strong>repository/</strong>: Реализации репозиториев для работы с данными.</li>
        </ul>
    </li>
    <li>📁 <strong>di/</strong>: Компоненты для внедрения зависимостей.
        <ul>
            <li><code>config.py</code>: Провайдер для создания конфигурации.</li>
            <li><code>db.py</code>: Провайдер для создания зависимостей для работы с БД.</li>
            <li><code>fast_stream.py</code>: Провайдер для создания зависимостей FastStream.</li>
        </ul>
    </li>
</ul>

</body>
</html>
