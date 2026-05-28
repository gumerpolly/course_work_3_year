import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

df = pd.read_excel('course_work_3_year/Курсовая 2025-2026.xlsx',
                   sheet_name='Бригадир',
                   skiprows=5)

df.columns = ['Реплика', 'Персонаж', 'Длина_реплики', 'Тип_речи',
              'К_кому', 'Обращение', 'Вопрос_ответ', 'Номер_реплики',
              'Эмоции', 'Согласие', 'С_кем', 'Столбец1']

characters = ["Бригадир", "Бригадирша", "Советник", "Советница", "Сын", "Софья", "Слуга", "Добролюбов"]

word_counts = {}
for character in characters:
    char_data = df[df['Персонаж'] == character]
    word_counts[character] = char_data['Длина_реплики'].sum()

centrality = {} # Центральность персонажа
for character in characters:
    to_whom = set(df[(df['Персонаж'] == character) & (df['Тип_речи'] == 'Д')]['К_кому'].dropna())
    from_whom = set(df[(df['К_кому'] == character) & (df['Тип_речи'] == 'Д')]['Персонаж'].dropna())
    all_connections = to_whom.union(from_whom)
    centrality[character] = len(all_connections)

# Визуализация
fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor('#f5f5f5')
ax.set_facecolor('#f0f0f0')

max_words = max(word_counts.values())
min_words = min(word_counts.values())

sizes = {}
for char, words in word_counts.items():
    if max_words == min_words:
        sizes[char] = 2500
    else:
        sizes[char] = 150 + (words - min_words) / (max_words - min_words) * 800

np.random.seed(42)

positions = {
    "Бригадир": (3, 5),
    "Бригадирша": (2, 3),
    "Советник": (4, 4),
    "Советница": (5, 3),
    "Сын": (4, 2),
    "Софья": (6, 4),
    "Слуга": (1, 1.5),
    "Добролюбов": (6, 2)
}

colors = plt.cm.viridis(np.array(list(centrality.values())) / max(centrality.values()))

char_colors = {char: colors[i] for i, char in enumerate(characters)}

# Рисуем пузырьки
patches = []
texts = []

for char in characters:
    x, y = positions[char]
    size = sizes[char]
    color = char_colors[char]

    circle = Circle((x, y), size / 1000, color=color, alpha=0.7, ec='black', linewidth=2)
    ax.add_patch(circle)
    patches.append(circle)

    text = ax.text(x, y, char, ha='center', va='center',
                   fontsize=10 + size / 500, fontweight='bold',
                   color='black')
    texts.append(text)

    annotation = f"{word_counts[char]} слов\n{centrality[char]} собеседников"
    ax.text(x, y - size / 1000 - 0.15, annotation, ha='center', va='top',
            fontsize=8, style='italic', bbox=dict(boxstyle='round,pad=0.3',
                                                  facecolor='white', alpha=0.7))

# Настройка графика
ax.set_xlim(0, 7.5)
ax.set_ylim(0, 6.5)
ax.set_aspect('equal')
ax.axis('off')

title_text = 'Анализ персонажей комедии "Бригадир"\nРазмер пузырька = количество произнесённых слов\nЦвет = центральность'
ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)

def get_sosednik_form(count):
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} собеседник"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return f"{count} собеседника"
    else:
        return f"{count} собеседников"

# Легенда для размера
legend_elements = []
example_sizes = [min(sizes.values()), (min(sizes.values()) + max(sizes.values()))/2, max(sizes.values())]
example_words = [min_words, (min_words + max_words)/2, max_words]

for size, words in zip(example_sizes, example_words):
    legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                       markerfacecolor='gray', markersize=np.sqrt(size/1000)*10,
                                       label=f'~{int(words)} слов'))

# Легенда для центральности
centrality_legend = []
for cent in [1, 3, 5, 7]:
    color = plt.cm.viridis(cent / 7)
    form = get_sosednik_form(cent)
    centrality_legend.append(plt.Line2D([0], [0], marker='s', color='w',
                                        markerfacecolor=color, markersize=10,
                                        label=form))


legend1 = ax.legend(handles=legend_elements, loc='upper left',
                    title='Количество слов', framealpha=0.9,
                    bbox_to_anchor=(0.02, 0.98))
legend2 = ax.legend(handles=centrality_legend, loc='upper right',
                    title='Центральность', framealpha=0.9,
                    bbox_to_anchor=(0.98, 0.98))
ax.add_artist(legend1)

plt.tight_layout()


plt.savefig('character_analysis_bubble_chart.png', dpi=300, bbox_inches='tight', facecolor='#f5f5f5')
plt.show()
