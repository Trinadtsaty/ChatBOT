# Ищу в сообщение числа.
def search_numbers(message:str):
    answer = []
    if message[0].isdigit():
        numbers = message[0]
    else:
        numbers = ''
    # print(numbers)
    # print(message[1:])
    for i, item in enumerate(message[1:]):
        if item.isdigit():
            numbers+=item
        elif item == '.':
            if item not in numbers:
                numbers+=item
            elif numbers != '':
                answer.append(float(numbers))
                numbers = ''
        elif numbers != '':
            answer.append(float(numbers))
            numbers = ''
    return answer



S = 'dfdsf'

print(search_numbers(S))
# print(float('12'))