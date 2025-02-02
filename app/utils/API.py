import httpx

from app.core.config import config


def luhn_checksum(imei: str) -> int:
    digits = [int(d) for d in imei]
    total = 0
    alt = False
    for d in reversed(digits):
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10


def is_valid_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False
    return luhn_checksum(imei) == 0


async def check_imei(imei: str) -> str:
    if not is_valid_imei(imei):
        return {"error": "Переданный IMEI некорректен"}

    headers = {
        "Authorization": "Bearer " + config.IMEI_CHECK_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {"deviceId": imei, "serviceId": config.SERVICE_ID}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.IMEI_CHECK_URL, headers=headers, json=payload
            )
            response.raise_for_status()
            result = response.json()
    except httpx.HTTPStatusError as e:
        result = {"error": f"Ошибка HTTP: {e.response.status_code} - {e.response.text}"}
    except httpx.RequestError as e:
        result = {"error": f"Ошибка запроса: {e}"}
    except Exception as e:
        result = {"error": str(e)}

    return format_imei_response(result)


def format_imei_response(data: dict) -> str:
    if "error" in data:
        return f"Ошибка: {data['error']}"

    props = data.get("properties", {})

    return (
        f"📱 Устройство: {props.get('deviceName', 'Неизвестно')}\n"
        f"🔢 IMEI: {props.get('imei', 'Нет данных')}\n"
        f"🆔 MEID: {props.get('meid', 'Нет данных')}\n"
        f"🔄 Замена устройства: {'✅ Да' if props.get('replacement') else '❌ Нет'}\n"
        f"🛠 Демо-устройство: {'✅ Да' if props.get('demoUnit') else '❌ Нет'}\n"
        f"💰 Стоимость проверки: {data.get('amount', 'Нет данных')}$\n"
        f"🚦 Блокировка в США: {props.get('usaBlockStatus', 'Нет данных')}\n"
        f"📍 Сеть: {props.get('network', 'Нет данных')}\n"
        f"🚫 В черном списке: {'✅ Да' if props.get('gsmaBlacklisted') else '❌ Нет'}\n\n"
        f"🖼 [Фото устройства]({props.get('image', '#' if props.get('image') else '' )})\n\n"
        f"⚠️ Внимание: Вы используете тестовые данные. Подробнее: [API Sandbox](https://imeicheck.net/developer-api)"
    )
