"""
Задачи:
Любой текст.

Высокая цель: уменшить размерность векторного представления слов текстуальных данных.Построить граифики уменьшения размерности. 
    
1. Загрузка текстового файла из корневого каталога.
2. Обработка текстовых данных.
3. Понижение размерности текстовых данных.
4. Построить график объема информации. 
5. Сколько компонент нужно оставить что бы сохранить 90% информации. 
6. Попробовать восстановить пару исходных слов. 

"""
from string import punctuation
import nltk, copy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import pymorphy2
import pandas as pd
import matplotlib.pyplot as plt

# Загрузить файл, прочитать его и сохранить текст в переменную text.
with open("Eugene_Piuta/DZ_03/file.txt", encoding='utf-8') as f:
    text = f.read()
print(f"text(500 символов): \n{text[:500]} \n\n***********************************\n")

# Удаление знаков пунктуации и цифр. Приводим текст в нижний регистр.
numbers = set(range(0, 10))
exclude = set(set(punctuation)|numbers)

# Добавим дополнительные знаки в исключения
exclude.update("…", "”", "”", "“", ",", "—")
text_new =copy.copy(text)
text_new = ''.join(ch for ch in text_new if ch not in exclude)
text_new = text_new.lower()
print(f"text_new(500 символов): \n{text_new[:500]}\n\n**************************************\n")

# Разбиваем текст на слова с помощью nltk
words_nlkt = word_tokenize(text_new, language="russian")
print(f"Количество слов: {len(words_nlkt)}\n\n*************************************\n")

# Удалим стоп-слова
stop_words = stopwords.words("russian")
words = [i for i in words_nlkt if i not in stop_words]
print(f"words(50 первых слов): \n{words[:50]}\n\n***********************************\n")

# Лемматизируем полученные слова с помощью pymorphy2
morph = pymorphy2.MorphAnalyzer()
words_morph = [morph.parse(i)[0].normal_form for i in words]
print(f"words_morph(50 первых слов): \n{words_morph[:50]}\n\n***********************************\n")

# Находим предложения с помощью nltk
sentences = sent_tokenize(text, language="russian")
print(f"sentences(5): \n{sentences[:5]}\n\n***********************************\n")


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
#Преобразование текстов в TF-IDF векторы
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
tfidf_matrix = tfidf_vectorizer.fit_transform(words_morph)
#Применение TruncatedSVD 
svd = TruncatedSVD(n_components=100)
reduced_tfidf = svd.fit_transform(tfidf_matrix)


import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
#Применение t-SNE для снижения размерности
tsne_text = TSNE(n_components=2, perplexity=30)
reduced_tsne_text = tsne_text.fit_transform(reduced_tfidf)
#Визуализация результата t-SNE
plt.figure(figsize=(10, 6))
plt.scatter(reduced_tsne_text[:, 0], reduced_tsne_text[:, 1], alpha=0.5)
plt.title('t-SNE Visualization of Text')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.show()



# Создаем экземпляр PCA 
from sklearn.decomposition import PCA
pca = PCA() 

# Обучаем PCA на данный reduced_tfidf
pca.fit(reduced_tfidf)

# Строим график объясненной дисперсии
explained_variance_ratio = pca.explained_variance_ratio_
plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, marker='o')
plt.xlabel("Число компонент")
plt.ylabel("Доля объясненной дисперсии")
plt.title("Метод локтя для выбора числа компонент")
plt.show()
# По графику видим, что оптимальное число компонент = 60



pca = PCA()
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(words_morph)

# Применение PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X.toarray())
# Визуализация результата PCA для текстовых данных
plt.figure(figsize=(10, 6))
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], alpha=0.5)
plt.title('PCA Visualization of Text Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()



# Создаем экземпляр PCA с заданным порогом
pca = PCA(0.9)  # сохраняем 90% доли объясненной дисперсии
pca.fit(reduced_tfidf)
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance = explained_variance_ratio.cumsum()

# Визуализация объясненной дисперсии
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o')
plt.xlabel("Число компонент")
plt.ylabel("Накопленная доля объясненной дисперсии")
plt.title("Анализ объясненной дисперсии")
plt.show()



# Используем NLP
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
# Выполним векторизацию наших входных данных и преобразуем их в массив NumPy для просмотра.
X = cv.fit_transform(sentences)
X = X.toarray()
# Выведем словарь сортированных слов по алфавиту:
print(f"словарь сортированных слов по алфавиту: \n{sorted(cv.vocabulary_.keys())[:50]}\n\n***********************************\n")

# Используем TF-IDF
tfidf = TfidfVectorizer()
# Преобразуем наши данные:
transformed = tfidf.fit_transform(sentences)
pd.set_option('display.notebook_repr_html', True)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 80)
# Создаем таблицу данных с названиями признаков, то есть со словами (в столбце индекса), отсортированными по показателям TF-IDF (в столбце показателей):
df = pd.DataFrame(transformed[0].T.todense(),
  index=tfidf.get_feature_names_out(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)



print(f"Таблица с названиями признаков: \n{df[:30]}\n\n***********************************\n")













#*************************
print(f"\n\n\n***********************************\n\n    *****  Работа завершена!  *****\n\n***********************************\n")

"""
Выводы:
Загрузили и обработали текcт. 
Понизили размерность тескта различными методами
Определили,что оптимальное число компонент = 60 c PCA, 10 c TF-IDF (оставить 90% информации. )
Восстановить слово в исходном тексте теоретически возможно используя рейтинг слов в последовательности.



Консоль:
text(500 символов): 
— Это как у тебя получилось, скажи-ка мне, — с прищуром спросил Ратибор.

— Эм, я не знаю, — пожал плечами я. — Просто само как-то. Дракон рядом оказался, я руку и протянул.

— Его-то к драконам тянет, — подтвердил Клим. — Его вообще ко всей животине тянет. Нравится она ему. Псы особенно.

— Опять та же песня, — покраснел от злости Джарек. — У него все само получилось, как всегда!

— Остынь, Джа, — рявкнул на него Ратибор. — Смотри какой контакт. Да Аврора чуть ли не мурлычет у него. Ты прекрасн

***********************************

text_new(500 символов):
 это как у тебя получилось скажика мне  с прищуром спросил ратибор

 эм я не знаю  пожал плечами я  просто само както дракон рядом оказался я руку и протянул

 егото к драконам тянет  подтвердил клим  его вообще ко всей животине тянет нравится она ему псы особенно

 опять та же песня  покраснел от злости джарек  у него все само получилось как всегда

 остынь джа  рявкнул на него ратибор  смотри какой контакт да аврора чуть ли не мурлычет у него ты прекрасно знаешь что это значит она и слушаться

**************************************

Количество слов: 1913

*************************************

words(50 первых слов):
['это', 'получилось', 'скажика', 'прищуром', 'спросил', 'ратибор', 'эм', 'знаю', 'пожал', 'плечами', 'просто', 'само', 'както', 'дракон', 'рядом', 'оказался', 'руку', 'протянул', 'егото', 'драконам', 'тянет', 'подтвердил', 'клим', 'вообще', 'ко', 'всей', 'животине', 'тянет', 'нравится', 'псы', 'особенно', 'та', 'песня', 'покраснел', 'злости', 'джарек', 'само', 'получилось', 'остынь', 'джа', 'рявкнул', 'ратибор', 'смотри', 'контакт', 'аврора', 'мурлычет', 'прекрасно', 'знаешь', 'это', 'значит']      

***********************************

words_morph(50 первых слов): 
['это', 'получиться', 'скажик', 'прищур', 'спросить', 'ратибор', 'эм', 'знать', 'пожать', 'плечо', 'просто', 'сам', 'както', 'дракон', 'рядом', 'оказаться', 'рука', 'протянуть', 'еготь', 'дракон', 'тянуть', 'подтвердить', 'клим', 'вообще', 'к', 'весь', 'животина', 'тянуть', 'нравиться', 'пёс', 'особенно', 'тот', 'песня', 'покраснеть', 'злость', 'джарек', 'сам', 'получиться', 'остыть', 'джа', 'рявкнуть', 'ратибор', 'смотреть', 'контакт', 'аврора', 'мурлыкать', 'прекрасно', 'знать', 'это', 'значит']  

***********************************

sentences(5):
['— Это как у тебя получилось, скажи-ка мне, — с прищуром спросил Ратибор.', '— Эм, я не знаю, — пожал плечами я.', '— Просто само как-то.', 'Дракон рядом оказался, я руку и протянул.', '— Его-то к драконам тянет, — подтвердил Клим.']

***********************************

словарь сортированных слов по алфавиту: 
['аврора', 'авроре', 'авророй', 'аврору', 'артиллерии', 'артиллерийского', 'артиллерию', 'артиллерия', 'атака', 'атаку', 'атакуешь', 'ах', 'аэродинамика', 'ба', 'бах', 'без', 'безопасно', 'беспрекословно', 'бешенства', 'благо', 'благодаря', 'ближайшая', 'ближе', 'близко', 'более', 'большая', 'большинство', 'больших', 'большой', 'боюсь', 'брали', 'брат', 'броневой', 'бросил', 'бросился', 'будем', 'будет', 'будто', 'будь', 'бы', 'был', 'была', 'были', 'было', 'быстрее', 'быстро', 'быть', 'вами', 'ваше', 'вверх']

***********************************

Таблица с названиями признаков:
                   TF-IDF
ка               0.380100
прищуром         0.380100
получилось       0.353985
скажи            0.353985
спросил          0.353985
тебя             0.299413
это              0.259543
мне              0.246170
как              0.246170
ратибор          0.238584
артиллерийского  0.000000
артиллерию       0.000000
артиллерия       0.000000
шире             0.000000
ах               0.000000
аэродинамика     0.000000
ба               0.000000
бах              0.000000
без              0.000000
безопасно        0.000000
беспрекословно   0.000000
бешенства        0.000000
благо            0.000000
благодаря        0.000000
ближайшая        0.000000
ближе            0.000000
близко           0.000000
более            0.000000
атаку            0.000000
большинство      0.000000

***********************************




***********************************

    *****  Работа завершена!  *****

***********************************




"""
