# <<<<<<< HEAD
import aiosqlite

async def user_profiles_db():
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS focus_time (
                user_id TEXT,
                date TEXT,
                total_time TEXT,
                PRIMARY KEY (user_id, date)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ai_responses (
                user_id TEXT,
                key TEXT,
                value TEXT
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
            CREATE TABLE IF NOT EXISTS ai_style (
                user_id TEXT,
                value TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS start_timer (
            user_id TEXT,
            time INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id TEXT,
                key TEXT,
                value TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                user_id TEXT,
                key TEXT,
                value TEXT
            )
        ''')
        await db.commit()

async def add_user_stats(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM user_stats WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO user_stats (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        await db.commit()

async def add_alarms(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM alarms WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO alarms (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        await db.commit()
async def get_alarms(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM alarms WHERE user_id = ? AND key = ?',
            (str(user_id),key)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None

async def add_ai_responses(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM ai_responses WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO ai_responses (user_id, key, value) VALUES (?,?,?)', (str(user_id),key, value))
        await db.commit()

async def get_ai_responses(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM ai_responses WHERE user_id = ? AND key = ?',
            (str(user_id),key)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None


async def add_time_start(user_id, time):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM start_timer WHERE user_id = ?', (str(user_id),))
        # await db.execute('DELETE FROM start_timer WHERE user_id = ? AND time = ?', (str(user_id),time))
        await db.execute('INSERT INTO start_timer VALUES (?,?)', (str(user_id),time) )
        await db.commit()

async def get_time_start(user_id):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT time FROM start_timer WHERE user_id = ?',
            (str(user_id),)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None

async def add_focus_time(user_id, date, total_time):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('''
        INSERT INTO focus_time (user_id, date, total_time) VALUES (?,?,?)
        ON CONFLICT (user_id, date)
        DO UPDATE SET total_time = total_time + excluded.total_time
        ''', (str(user_id), date, total_time))
        await db.commit()
        # await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
        # await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        # await db.commit()

async def add_user_facts(user_id, key, value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
        await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
        await db.commit()


async def get_user_facts(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM user_facts WHERE user_id = ? AND key = ?',
            (str(user_id),key)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None

async def add_ai_style(user_id,value):
    async with aiosqlite.connect('user_profiles.db') as db:
        await db.execute('DELETE FROM ai_style WHERE user_id = ?', (str(user_id),) )
        await db.execute('INSERT INTO ai_style (user_id, value) VALUES (?,?)', (str(user_id),value))
        await db.commit()
async def get_ai_style(user_id):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM ai_style WHERE user_id = ?',
            (str(user_id),)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return None


async def get_all_user_facts(user_id):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT key, value FROM user_facts WHERE user_id = ?', (str(user_id),)
        ) as cursor:
            rows = await cursor.fetchall()
            if rows:
                return rows
            return None

async def get_user_stats(user_id, key):
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute(
            'SELECT value FROM user_stats WHERE user_id = ? AND key = ?',
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
# =======
# import aiosqlite
#
# async def user_profiles_db():
#     async with aiosqlite.connect('user_profiles.db') as db:
#         await db.execute('''
#             CREATE TABLE IF NOT EXISTS focus_time (
#                 user_id TEXT,
#                 date TEXT,
#                 total_time TEXT
#             )
#         ''')
#         await db.execute('''
#             CREATE TABLE IF NOT EXISTS user_facts (
#                 user_id TEXT,
#                 key TEXT,
#                 value TEXT
#             )
#         ''')
#         await db.execute('''
#             CREATE TABLE IF NOT EXISTS reminders (
#                 user_id TEXT,
#                 key TEXT,
#                 value TEXT
#             )
#         ''')
#         await db.commit()
#
# async def add_reminder(user_id, key, value):
#     async with aiosqlite.connect('user_profiles.db') as db:
#         await db.execute('DELETE FROM reminders WHERE user_id = ? AND key = ?', (str(user_id),key))
#         await db.execute('INSERT INTO reminders (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
#         await db.commit()
#
#
# async def add_focus_time(user_id, date, duration):
#     async with aiosqlite.connect('focus_times.db') as db:
#         await db.execute('''
#         INSERT INTO focus_times (user_id, date, duration) VALUES (?,?,?)
#         ON CONFLICT (user_id, date)
#         DO UPDATE SET total_time = total_time + excluded.total_time
#         '''
#         )
#         await db.commit()
#         # await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
#         # await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
#         # await db.commit()
#
# async def add_user_facts(user_id, key, value):
#     async with aiosqlite.connect('user_profiles.db') as db:
#         print(f"DEBUG: Сохраняю в БД: юзер {user_id}, ключ {key}, значение {value}")
#         # await db.execute('INSERT OR REPLACE INTO user_facts (user_id, key, value) VALUES (?, ?, ?)',
#         #                  (str(user_id), key, value))
#         await db.execute('DELETE FROM user_facts WHERE user_id = ? AND key = ?', (str(user_id),key))
#         await db.execute('INSERT INTO user_facts (user_id, key, value) VALUES (?,?,?)', (str(user_id),key,value))
#
#         await db.commit()
#
#
# async def get_user_facts(user_id, key):
#     async with aiosqlite.connect('user_profiles.db') as db:
#         uid = str(user_id)
#         # Убрали лишние пробелы и сложности, чтобы увидеть, найдет ли он хоть что-то
#         sql = "SELECT value FROM user_facts WHERE user_id=? AND key=?"
#         # async with db.execute(sql, (uid, key)) as cursor:
#         #     row = await cursor.fetchone()
#         #     print(f"DEBUG: Поиск по {uid} и {key}. Результат: {row}")
#         #     return row[0] if row else None
#         # async with db.execute('SELECT * FROM user_facts') as cursor:
#         #     all_rows = await cursor.fetchall()
#         #     print(f"DEBUG: ВСЕ записи в базе: {all_rows}")
#         #     async with db.execute('SELECT value FROM user_facts WHERE user_id = ? AND key = ?',
#         #                           (str(user_id), key)) as cursor:
#         #         row = await cursor.fetchone()
#         #         return row[0] if row else None
#         async with db.execute(
#             'SELECT value FROM user_facts WHERE user_id = ? AND key = ?',
#             (str(user_id),key)
#         ) as cursor:
#             row = await cursor.fetchone()
#             print(f"DEBUG: Читаю из БД: найдено {row}")
#             if row:
#                 return row[0]
#             return None
#
# async def get_user_reminder(user_id, key):
#     async with aiosqlite.connect('user_profiles.db') as db:
#         async with db.execute(
#             'SELECT value FROM reminders WHERE user_id = ? AND key = ?',
#             (str(user_id),key)
#         ) as cursor:
#             row = await cursor.fetchone()
#             if row:
#                 return row[0]
#             return None
#
# async def get_user_time(user_id, date):
#     async with aiosqlite.connect('user_profiles.db') as db:
#         async with db.execute(
#             'SELECT total_time FROM focus_time WHERE user_id = ? AND date = ?',
#             (str(user_id),date)
#         ) as cursor:
#             row = await cursor.fetchone()
#             if row:
#                 return row[0]
#             return None
# >>>>>>> c7dd31ba49196073f193837bfba9ec795baae08d
