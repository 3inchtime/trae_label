from fastapi import APIRouter
from ..schemas import NumberToChineseRequest, NumberToChineseResponse

router = APIRouter(prefix="/number-to-chinese", tags=["number-to-chinese"])


def number_to_chinese(num):
    digits = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    units = ['', '拾', '佰', '仟']
    big_units = ['', '万', '亿', '兆']
    
    if num == 0:
        return '零元整'
    
    if num < 0:
        return '负' + number_to_chinese(abs(num))
    
    integer_part = int(num)
    decimal_part = int(round((num - integer_part) * 100))
    
    result = ''
    
    if integer_part > 0:
        integer_str = str(integer_part)
        length = len(integer_str)
        zero_flag = False
        
        for i, digit in enumerate(integer_str):
            d = int(digit)
            pos = length - 1 - i
            unit_pos = pos % 4
            big_unit_pos = pos // 4
            
            if d == 0:
                zero_flag = True
                if unit_pos == 0 and big_unit_pos > 0:
                    result += big_units[big_unit_pos]
            else:
                if zero_flag:
                    result += '零'
                    zero_flag = False
                result += digits[d] + units[unit_pos]
                if unit_pos == 0 and big_unit_pos > 0:
                    result += big_units[big_unit_pos]
        
        result += '元'
    
    if decimal_part > 0:
        jiao = decimal_part // 10
        fen = decimal_part % 10
        
        if jiao > 0:
            result += digits[jiao] + '角'
        elif integer_part > 0 and fen > 0:
            result += '零'
        
        if fen > 0:
            result += digits[fen] + '分'
    else:
        result += '整'
    
    return result


@router.post("", response_model=NumberToChineseResponse)
def convert_number_to_chinese(request: NumberToChineseRequest):
    chinese = number_to_chinese(request.number)
    return NumberToChineseResponse(
        number=request.number,
        chinese=chinese
    )
