from faster_whisper import WhisperModel
import sys
import os

def transcribe_audio(audio_path, model_size="base", device="cpu", compute_type="int8"):
    """
    Функция для транскрибации аудиофайла.

    Параметры:
    audio_path (str): Путь к аудиофайлу.
    model_size (str): Размер модели ('tiny', 'base', 'small', 'medium', 'large-v3').
    device (str): 'cpu' или 'cuda' (если есть NVIDIA GPU).
    compute_type (str): Тип вычислений ('int8', 'float16', 'float32').
    """
    if not os.path.exists(audio_path):
        print(f"Ошибка: Файл '{audio_path}' не найден.")
        return

    print(f"Загрузка модели '{model_size}'...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print("Начинаю транскрибацию...")
    segments, info = model.transcribe(audio_path, beam_size=5, language="ru")

    print(f"Обнаруженный язык: '{info.language}', вероятность: {info.language_probability:.2f}")
    print("\n--- Стенограмма ---")

    # Базовый вывод в консоль
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    print("--- Конец стенограммы ---")

    output_file = os.path.splitext(audio_path)[0] + "_transcript.txt"
    print(f"\nСохраняю стенограмму в файл: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        # Повторно получаем генератор segments (он был исчерпан при первом проходе)
        segments, _ = model.transcribe(audio_path, beam_size=5, language="ru")
        for segment in segments:
            f.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))
    print("Готово!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python transcribe.py <путь_к_аудиофайлу>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Вы можете изменить параметры модели здесь
    transcribe_audio(
        audio_path=input_file,
        model_size="small",  # Выберите модель: 'tiny', 'base', 'small', 'medium', 'large-v3'
        device="cpu",  # 'cpu' или 'cuda' если есть NVIDIA GPU
        compute_type="int8"  # 'int8', 'float16', 'float32'
    )

