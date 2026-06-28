import aiosqlite

async def user_profiles_db():
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS focus_time (
                user_id TEXT,
                date TEXT,
                total_time TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_facts (
                user_id TEXT,
                key TEXT,
                value TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                user_id TEXT,
                key TEXT,
                value TEXT
            )
        ''')
        await db.commit()

async def add_reminder(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM reminders WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO reminders (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        await db.commit()


async def add_focus_time(user_id, date, duration):
    async with aiosqlite.connect('focus_times.db') as db:
        await db.execute('''
        INSERT INTO focus_times (user_id, date, duration) VALUES (?,?,?)
        ON CONFLICT (user_id, date)
        DO UPDATE SET total_time = total_time + excluded.total_time
        '''
        )
        await db.commit()
        # await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
        # await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        # await db.commit()

async def add_user_facts(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        print(f"DEBUG: Сохраняю в БД: юзер {user_id}, ключ {key}, значение {value}")
        # await db.execute('INSERT OR REPLACE INTO user_facts (user_id, key, value) VALUES (?, ?, ?)',
        #                  (str(user_id), key, value))
        await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))

        await db.commit()


async def get_user_facts(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        uid = str(user_id)
        # Убрали лишние пробелы и сложности, чтобы увидеть, найдет ли он хоть что-то
        sql = "SELECT value FROM user_facts WHERE user_id=? AND key=?"
        # async with db.execute(sql, (uid, key)) as cursor:
        #     row = await cursor.fetchone()
        #     print(f"DEBUG: Поиск по {uid} и {key}. Результат: {row}")
        #     return row[0] if row else None
        # async with db.execute('SELECT * FROM user_facts') as cursor:
        #     all_rows = await cursor.fetchall()
        #     print(f"DEBUG: ВСЕ записи в базе: {all_rows}")
        #     async with db.execute('SELECT value FROM user_facts WHERE user_id = ? AND key = ?',
        #                           (str(user_id), key)) as cursor:
        #         row = await cursor.fetchone()
        #         return row[0] if row else None
        async with db.execute(
            'SELECT value FROM user_facts WHERE user_id = ? AND key = ?',
            (str(user_id),key)
        ) as cursor:
            row = await cursor.fetchone()
            print(f"DEBUG: Читаю из БД: найдено {row}")
            if row:
                return row[0]
            return None

async def get_user_reminder(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM reminders WHERE user_id = ? AND key = ?',
            (str(user_id),key)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None

async def get_user_time(user_id, date):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT total_time FROM focus_time WHERE user_id = ? AND date = ?',
            (str(user_id),date)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None
