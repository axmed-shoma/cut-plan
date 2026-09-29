import io
import base64
import IPython.display as display
import numpy as np
import pandas as pd

def safe_float(value):
    return float(str(value).replace(',', '.'))

def _calculate_plan_data(start_width, end_width, total_length, piece_length, last_piece_length, direction_reverse=False):
    total_width_difference = start_width - end_width
    results_data = []

    count = int((total_length - last_piece_length) / piece_length)
    OFFSET = 0.5  # см — нахлёст между кусками

    if direction_reverse:
        curr = end_width
        width_change_per_piece = total_width_difference * (piece_length / total_length)
        for i in range(count):
            if i > 0:
                curr -= OFFSET  # каждый следующий кусок уже на 0.5 см
            prev_curr_for_display = curr
            curr += width_change_per_piece
            curr = round(curr * 2) / 2
            results_data.append({
                'Кусок': i + 1,
                'Длина (м)': piece_length,
                'Ширина от (см)': prev_curr_for_display,
                'Ширина до (см)': curr
            })
        # Последний кусок
        curr -= OFFSET
        prev_curr_for_display = curr
        final_curr = start_width
        results_data.append({
            'Кусок': count + 1,
            'Длина (м)': last_piece_length,
            'Ширина от (см)': prev_curr_for_display,
            'Ширина до (см)': final_curr
        })
    else:
        curr = start_width
        width_change_per_piece = total_width_difference * (piece_length / total_length)
        for i in range(count):
            if i > 0:
                curr += OFFSET  # каждый следующий кусок шире на 0.5 см
            prev_curr_for_display = curr
            curr -= width_change_per_piece
            curr = round(curr * 2) / 2
            results_data.append({
                'Кусок': i + 1,
                'Длина (м)': piece_length,
                'Ширина от (см)': prev_curr_for_display,
                'Ширина до (см)': curr
            })
        # Последний кусок
        curr += OFFSET
        prev_curr_for_display = curr
        final_curr = end_width
        results_data.append({
            'Кусок': count + 1,
            'Длина (м)': last_piece_length,
            'Ширина от (см)': prev_curr_for_display,
            'Ширина до (см)': final_curr
        })
    return results_data

def simple_plan():
    try:
        start = safe_float(input("Старт (см) [широкий конец]: "))
        end = safe_float(input("Финиш (см) [узкий конец]: "))
        total_l = safe_float(input("Общая длина (м): "))
        piece_l = safe_float(input("Длина куска (м): "))
        last_l = safe_float(input("Длина последнего (м): "))

        direction_input = input("Направление расчета (прямой/обратный): ").lower().strip()
        direction_reverse = (direction_input == 'обратный')
    except ValueError:
        print("Вводи только числа!")
        return

    if start <= end:
        print("Ошибка: Ширина 'Старт' должна быть больше ширины 'Финиш' для расчета уклона.")
        return
    if total_l <= 0 or piece_l <= 0 or last_l <= 0:
        print("Ошибка: Длины должны быть положительными числами.")
        return
    if (piece_l * int((total_l - last_l) / piece_l) + last_l) > (total_l + 0.001):
        print("Ошибка: Сумма длин кусков превышает общую длину. Проверьте Длина куска и Длина последнего.")
        return

    plan_data = _calculate_plan_data(start, end, total_l, piece_l, last_l, direction_reverse)

    df_results = pd.DataFrame(plan_data)
    display.display(df_results)

    csv_filename = 'cut_plan_results.csv'
    df_results.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"Результаты расчетов сохранены в файл: {csv_filename}")

if __name__ == "__main__":
    simple_plan()
