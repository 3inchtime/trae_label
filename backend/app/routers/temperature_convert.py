from fastapi import APIRouter, HTTPException
from ..schemas import TemperatureConvertRequest, TemperatureConvertResponse

router = APIRouter(prefix="/temperature", tags=["temperature"])

TEMPERATURE_UNITS = ['celsius', 'fahrenheit', 'kelvin', 'rankine']


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def celsius_to_rankine(celsius):
    return (celsius + 273.15) * 9 / 5


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def rankine_to_celsius(rankine):
    return rankine * 5 / 9 - 273.15


def convert_to_celsius(value, from_unit):
    if from_unit == 'celsius':
        return value
    elif from_unit == 'fahrenheit':
        return fahrenheit_to_celsius(value)
    elif from_unit == 'kelvin':
        return kelvin_to_celsius(value)
    elif from_unit == 'rankine':
        return rankine_to_celsius(value)
    raise HTTPException(status_code=400, detail=f"不支持的单位: {from_unit}")


def convert_from_celsius(celsius, to_unit):
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return celsius_to_fahrenheit(celsius)
    elif to_unit == 'kelvin':
        return celsius_to_kelvin(celsius)
    elif to_unit == 'rankine':
        return celsius_to_rankine(celsius)
    raise HTTPException(status_code=400, detail=f"不支持的单位: {to_unit}")


@router.post("/convert", response_model=TemperatureConvertResponse)
def convert_temperature(request: TemperatureConvertRequest):
    if request.from_unit not in TEMPERATURE_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.from_unit}")
    if request.to_unit not in TEMPERATURE_UNITS:
        raise HTTPException(status_code=400, detail=f"不支持的单位: {request.to_unit}")

    celsius = convert_to_celsius(request.value, request.from_unit)
    result = convert_from_celsius(celsius, request.to_unit)

    return TemperatureConvertResponse(
        value=request.value,
        from_unit=request.from_unit,
        to_unit=request.to_unit,
        result=round(result, 4)
    )
