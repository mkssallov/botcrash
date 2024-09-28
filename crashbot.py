import requests
from bs4 import BeautifulSoup
import statistics
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CoefficientFetcher:
    """Класс для получения коэффициентов с веб-страницы."""
    
    def __init__(self, url):
        self.url = url
        self.coefficients = []

    def fetch_coefficients(self):
        """Получает коэффициенты с указанного URL."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            soup = BeautifulSoup(response.text, 'html.parser')

            # Пример поиска коэффициентов (необходимо адаптировать под структуру страницы)
            for item in soup.find_all('div', class_='coefficient-class'):  # Замените 'coefficient-class' на правильный класс
                self.coefficients.append(float(item.text.strip()))
            logging.info(f"Получено коэффициентов: {len(self.coefficients)}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при получении коэффициентов: {e}")
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")

class CrashPredictor:
    """Класс для прогнозирования следующего коэффициента."""
    
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def predict_next_coefficient(self):
        """Прогнозирует следующий коэффициент на основе последних пяти значений."""
        if len(self.coefficients) < 5:
            return None, 0  # Невозможно предсказать

        last_five = self.coefficients[-5:]
        prediction = sum(last_five) / len(last_five)  # Среднее значение
        accuracy = statistics.stdev(last_five) / prediction if prediction != 0 else 0  # Оценка точности
        return prediction, accuracy

    def display_prediction(self):
        """Выводит прогноз и точность."""
        prediction, accuracy = self.predict_next_coefficient()
        if prediction is not None:
            logging.info(f"Прогноз следующего коэффициента: {prediction:.2f}")
            logging.info(f"Точность прогноза: {accuracy:.2%}")
        else:
            logging.warning("Недостаточно данных для прогноза.")

def main():
    code = input("Введите код доступа: ")
    if code != "085432":
        logging.error("Неверный код доступа.")
        return

    url = "https://1wcght.life/casino/play/1play_1play_fastcrash"  # Замените на актуальный URL
    fetcher = CoefficientFetcher(url)
    
    fetcher.fetch_coefficients()
    predictor = CrashPredictor(fetcher.coefficients)
    predictor.display_prediction()

if __name__ == "__main__":
    main()

