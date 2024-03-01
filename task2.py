def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1

        # інакше x присутній на позиції і повертаємо кортеж з кількістю ітерацій та "верхньою межею"
        else:
            return (iterations, arr[mid])

    # якщо елемент не знайдений, повертаємо кортеж з кількістю ітерацій та "верхньою межею"
    return (iterations, arr[high] if high >= 0 else None)

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
x = 5
result = binary_search(arr, x)
print("Кількість ітерацій:", result[0])
print("Верхня межа:", result[1])
