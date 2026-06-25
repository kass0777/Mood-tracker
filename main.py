import datetime
import os
import ollama


def get_ai_analysis(journal_text):
    """Отправляет текст дня в Ollama для анализа настроения."""
    system_instruction = (
        "Ты — чуткий ИИ-психолог и аналитик настроения. Проанализируй текст дневника пользователя за день. "
        "Выведи ответ СТРОГО по следующему шаблону (не добавляй ничего лишнего от себя):\n\n"
        "📊 ОЦЕНКА НАСТРОЕНИЯ: [Поставь оценку от 1 до 10, где 1 - глубокая депрессия/стресс, 10 - абсолютное счастье]\n"
        "🎭 ОСНОВНЫЕ ЭМОЦИИ: [Перечисли 2-3 главные эмоции через запятую]\n"
        "🔑 КЛЮЧЕВЫЕ СОБЫТИЯ: [Кратко в одну строку, что произошло за день]\n"
        "💡 СЛОВО ПОДДЕРЖКИ: [Напиши одну теплую, мотивирующую или поддерживающую фразу для пользователя]"
    )

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Вот моя запись за сегодня:\n\"{journal_text}\""}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Не удалось подключиться к Ollama: {e}"


def run_mood_tracker():
    print("✨ Добро пожаловать в твой личный ИИ-Дневник Настроения ✨")
    print("Вся информация хранится локально и полностью конфиденциальна.\n")

    # 1. Спрашиваем пользователя, как прошел день
    print("Как прошёл твой день? Опиши свои мысли, чувства или события (нажмите Enter для завершения записи):")
    user_entry = input("> ")

    if not user_entry.strip():
        print("Запись пустая. Программа завершена.")
        return

    print("\n🤖 ИИ анализирует твое настроение...")
    ai_analysis = get_ai_analysis(user_entry)

    # 2. Формируем красивую дату
    today_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 3. Собираем итоговый текст для сохранения
    entry_layout = (
        f"=========================================\n"
        f"📅 ДАТА И ВРЕМЯ: {today_str}\n"
        f"=========================================\n"
        f"📝 ТВОЯ ЗАПИСЬ:\n{user_entry}\n\n"
        f"🤖 АНАЛИЗ ИИ:\n{ai_analysis}\n"
        f"=========================================\n\n"
    )

    # 4. Выводим анализ на экран
    print("\n" + ai_analysis + "\n")

    # 5. Сохраняем в локальный файл-дневник
    file_name = "my_mood_diary.txt"
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(entry_layout)

    print(f"✅ Запись успешно проанализирована и сохранена в файл '{file_name}'!")


if __name__ == "__main__":
    run_mood_tracker()