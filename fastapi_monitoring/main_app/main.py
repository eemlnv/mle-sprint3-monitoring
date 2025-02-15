from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram
import numpy as np

# создание экземпляра FastAPI приложения
app = FastAPI()

np.random.seed(1702)

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# main_app_predictions — объект метрики
main_app_predictions = Histogram(
    # имя метрики
    "main_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets=(1, 2, 4, 5, 10)
) 

# ваш код здесь — объект для сбора метрики
main_app_positive_predictions = Counter(
    # имя метрики
    "main_app_positive_predictions",
    # описание метрики
    "Histogram of positive predictions",
)

# предсказания
@app.get("/predict")
def predict(x: int, y: int):
    #print(x)
    np.random.seed(int(abs(x)))
    prediction = x+y + np.random.normal(0,1)
    main_app_predictions.observe(prediction) 
    # ваш код здесь — увеличение метрики счётчика
    if prediction > 0:
        main_app_positive_predictions.inc()
    return {'prediction': prediction}
