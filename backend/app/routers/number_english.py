from fastapi import APIRouter
from ..schemas import NumberToEnglishRequest, NumberToEnglishResponse

router = APIRouter(prefix="/number-to-english", tags=["number-to-english"])


def number_to_words(num):
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 
             'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion']
    
    if num == 0:
        return 'Zero'
    
    result = ''
    thousand_counter = 0
    
    while num > 0:
        if num % 1000 != 0:
            part = ''
            hundreds = (num % 1000) // 100
            remainder = num % 100
            
            if hundreds > 0:
                part += ones[hundreds] + ' Hundred '
            
            if remainder > 0:
                if remainder < 10:
                    part += ones[remainder]
                elif remainder < 20:
                    part += teens[remainder - 10]
                else:
                    part += tens[remainder // 10]
                    if remainder % 10 > 0:
                        part += '-' + ones[remainder % 10]
            
            result = part.strip() + ' ' + thousands[thousand_counter] + ' ' + result
        
        num = num // 1000
        thousand_counter += 1
    
    return result.strip()


def number_to_english(num):
    if num < 0:
        return 'Negative ' + number_to_english(abs(num))
    
    integer_part = int(num)
    decimal_part = int(round((num - integer_part) * 100))
    
    result = ''
    
    if integer_part > 0:
        result += number_to_words(integer_part) + ' Dollar'
        if integer_part != 1:
            result += 's'
    
    if decimal_part > 0:
        if integer_part > 0:
            result += ' and '
        result += number_to_words(decimal_part) + ' Cent'
        if decimal_part != 1:
            result += 's'
    elif integer_part == 0:
        result = 'Zero Dollars'
    
    return result


@router.post("", response_model=NumberToEnglishResponse)
def convert_number_to_english(request: NumberToEnglishRequest):
    english = number_to_english(request.number)
    return NumberToEnglishResponse(
        number=request.number,
        english=english
    )
