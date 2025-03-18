import asyncio
import os
from smartcard.System import readers

# Маппинг UID на последовательности Siri Shortcuts
TARGETS = {
    "04:01:02:AA:83:6B:85": ["SHORTCUT_A", "SHORTCUT_B"],
    "04:00:03:AA:83:6B:85": ["SHORTCUT_C", "SHORTCUT_D"],
    "04:01:06:AA:83:6B:85": ["SHORTCUT_E", "SHORTCUT_F"]
}

# Глобальный словарь для учета количества срабатываний UID
uid_counter = {}

# Максимальное количество сканирований для одной метки
SCAN_LIMIT = 2

async def read_nfc():
    """Асинхронное чтение UID с NFC"""
    r = readers()
    if not r:
        print("Нет доступных считывателей NFC.")
        return

    reader = r[0]  # Используем первый доступный ридер
    connection = reader.createConnection()
    connection.connect()

    SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Команда получения UID

    while True:
        try:
            # Асинхронное выполнение команды
            uid_data = await asyncio.to_thread(connection.transmit, SELECT)
            uid, sw1, sw2 = uid_data
            uid_str = ":".join(format(x, "02X") for x in uid)  # Преобразуем UID в строку с разделением ":"

            # Проверка наличия UID в TARGETS
            if uid_str in TARGETS:
                # Если UID найден, увеличиваем счетчик
                if uid_str not in uid_counter:
                    uid_counter[uid_str] = 1
                else:
                    uid_counter[uid_str] += 1

                print(f"UID: {uid_str} | Сканирование #{uid_counter[uid_str]}")

                # Запуск соответствующих Siri Shortcuts
                shortcut_list = TARGETS[uid_str]
                if uid_counter[uid_str] <= SCAN_LIMIT:
                    # Определяем, какой ярлык запускать в зависимости от количества срабатываний
                    shortcut_name = shortcut_list[uid_counter[uid_str] - 1]
                    await run_shortcut(shortcut_name)
                else:
                    print(f"UID {uid_str} больше не активен.")

            else:
                print(f"UID {uid_str} не найден в маппинге.")

            await asyncio.sleep(0.3)  # Короткая задержка перед следующим сканированием

        except Exception as e:
            print(f"Ошибка NFC: {e}")
            await asyncio.sleep(2)  # Ожидание перед новой попыткой

async def run_shortcut(shortcut_name):
    """Асинхронный запуск Siri Shortcuts через osascript"""
    print(f"Запуск ярлыка: {shortcut_name}")
    cmd = f'osascript -e "tell application \\"Shortcuts Events\\" to run shortcut \\"{shortcut_name}\\""'
    await asyncio.to_thread(os.system, cmd)

async def main():
    """Запуск основного цикла"""
    await read_nfc()

if __name__ == "__main__":
    asyncio.run(main())
