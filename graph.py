from pyvis.network import Network
import pandas as pd

df = pd.read_excel('course_work_3_year/Курсовая 2025-2026.xlsx',
                   sheet_name='Бригадир',
                   skiprows=5)

df.columns = ['Реплика', 'Персонаж', 'Длина_реплики', 'Тип_речи',
              'К_кому', 'Обращение', 'Вопрос_ответ', 'Номер_реплики',
              'Эмоции', 'Согласие', 'С_кем', 'Столбец1']

net = Network(directed=True, height="750px", width="100%")

net.set_options("""
{
  "edges": {
    "arrows": {
      "to": {
        "enabled": true,
        "type": "arrow"
      }
    },
    "smooth": {
      "enabled": true,
      "type": "curvedCW"
    }
  },
  "physics": {
    "enabled": true,
    "solver": "repulsion"
  },
  "nodes": {
    "size": 25,
    "font": {
      "size": 16
    }
  }
}
""")

net.add_nodes(
    ["Бригадир", "Бригадирша", "Советник", "Советница", "Сын", "Софья", "Слуга", "Добролюбов"],
    label=["Бригадир", "Бригадирша", "Советник", "Советница", "Сын", "Софья", "Слуга", "Добролюбов"],
    color=['#d47415', '#22b512', '#42adf5', '#4a21b0', '#e627a3', '#eed5b7', '#98f5ff', '#cdaa7d']
)


complex_pairs = {}

agreement_pairs = {}
disagreement_pairs = {}

for index, row in df.iterrows():
    person = row['Персонаж']
    speech_type = row['Тип_речи']
    to_whom = row['К_кому']
    agreement = row['Согласие']
    with_whom = row['С_кем']

    # Обработка основной связки (кто кому говорит)
    if pd.notna(person) and pd.notna(to_whom) and speech_type == 'Д':
        pair = f"{person}_{to_whom}"
        complex_pairs[pair] = complex_pairs.get(pair, 0) + 1

    # Обработка согласия/несогласия (если есть данные)
    if pd.notna(person) and pd.notna(with_whom) and agreement != '-' and pd.notna(agreement):
        agreement_pair = f"{person}_{with_whom}"

        if agreement == 'Согласие':
            agreement_pairs[agreement_pair] = agreement_pairs.get(agreement_pair, 0) + 1
        elif agreement == 'Несогласие':
            disagreement_pairs[agreement_pair] = disagreement_pairs.get(agreement_pair, 0) + 1


# Функция для определения цвета ребра на основе согласия/несогласия
def get_edge_color(person, to_whom):
    pair = f"{person}_{to_whom}"

    agree_count = agreement_pairs.get(pair, 0)
    disagree_count = disagreement_pairs.get(pair, 0)
    total = agree_count + disagree_count

    if total == 0:
        return '#888888'  # Серый цвет

    agree_percentage = (agree_count / total) * 100

    if agree_percentage > 50:
        return '#22b512'  # Зелёный (согласен > 50%)
    elif agree_percentage < 50:
        return '#ff3333'  # Красный (несогласен > 50%)
    else:
        return '#ffaa00'  # Жёлтый (ровно 50% = нейтральный)


for pair, count in sorted(complex_pairs.items(), key=lambda x: x[1], reverse=True):
    person, to_whom = pair.split('_')

    person = person.strip()
    to_whom = to_whom.strip()

    edge_color = get_edge_color(person, to_whom)

    net.add_edge(person, to_whom,
                 width=count * 0.3,
                 color=edge_color,
                 title=f"Реплик: {count}")

net.show('graph.html', notebook=False)
