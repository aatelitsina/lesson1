answers = [
    {"привет": "И тебе привет!", "как дела": "Лучше всех", "пока": "Увидимся"},
    {"что задали": "Не знаю", "кто знает": "Рома", "спасибо": "Пжл"}
    ]
def get_answer(question,ans=answers):
        if ans[0] is not None:
          res = ans[0].index(question]
        else:
            res = ans[1]question)
        return res


print(get_answer('Кто Знает'.lower()))