from skysmart.skysmart_api import SkySmartApi
from secret import token
from bs4 import BeautifulSoup
import base64

SSApi = SkySmartApi(token)


def remove_linebreaks(string: str) -> str:
    while '\n\n' in string:
        string = string.replace('\n\n', '\n')
    return string.strip()
class TaskAnswerObject:
    def __init__(self, task_hash):
        self.task_hash = task_hash

    def get_answers(self):
        """Получить все ответы на задания из теста"""
        answers = []
        tasks_len = 0
        tasks_uuid = SSApi.get_tasks(self.task_hash)
        for uuid in tasks_uuid:
            tasks_len += 1
            soup = SSApi.get_task_content(uuid)
            answers.append(self.get_task_answer(BeautifulSoup(soup, 'html.parser'), tasks_len))
        return answers

    def get_task_question(self, soup):
        """Получить вопрос из задания в тесте"""
        return soup.find('vim-instruction').text.strip()


    def get_full_question(self, soup):
        """Получить всё задание (вопрос, картинки и так далее...)"""
        elements = soup.find_all(
            ['vim-instruction', 'vim-groups', 'vim-test-item', 'vim-order-sentence-verify-item', 'vim-input-answers',
             'vim-select-item', 'vim-test-image-item', 'math-input-answer', 'vim-dnd-text-drop', 'vim-dnd-group-drag',
             'vim-groups-row', 'vim-strike-out-item', 'vim-dnd-image-set-drag', 'vim-dnd-image-drag',
             'edu-open-answer'])
        for element in elements:
            element.extract()
        return remove_linebreaks(soup.text)

    def get_task_answer(self, soup) -> dict:
        """Получить ответ на отдельное задание из теста"""
        answers = []
        soup = BeautifulSoup(soup, 'html.parser')

        if soup.find('vim-test-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
                answers.append(i.text)

        if soup.find('vim-order-sentence-verify-item'):
            for i in soup.find_all('vim-order-sentence-verify-item'):
                answers.append(i.text)

        if soup.find('vim-input-answers'):
            for i in soup.find_all('vim-input-answers'):
                answers.append(i.find('vim-input-item').text)

        if soup.find('vim-select-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
                answers.append(i.text)

        if soup.find('vim-test-image-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
                answers.append(f'{i.text} - Верный')

        if soup.find('math-input-answer'):
            for i in soup.find_all('math-input-answer'):
                answers.append(i.text)

        if soup.find('vim-dnd-text-drop'):
            for i in soup.find_all('vim-dnd-text-drop'):
                for f in soup.find_all('vim-dnd-text-drag'):
                    if i['drag-ids'] == f['answer-id']:
                        answers.append(f'{f.text}')

        if soup.find('vim-dnd-group-drag'):
            for i in soup.find_all('vim-dnd-group-drag'):
                for f in soup.find_all('vim-dnd-group-item'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f.text} - {i.text}')

        if soup.find('vim-groups-row'):
            for i in soup.find_all('vim-groups-row'):
                for l in i.find_all('vim-groups-item'):
                    try:
                        answers.append(f"{base64.b64decode(l['text']).decode('utf-8')}")
                    except:
                        pass

        if soup.find('vim-strike-out-item'):
            for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
                answers.append(i.text)

        if soup.find('vim-dnd-image-set-drag'):
            for i in soup.find_all('vim-dnd-image-set-drag'):
                for f in soup.find_all('vim-dnd-image-set-drop'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f["image"]} - {i.text}')

        if soup.find('vim-dnd-image-drag'):
            for i in soup.find_all('vim-dnd-image-drag'):
                for f in soup.find_all('vim-dnd-image-drop'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f.text} - {i.text}')

        if soup.find('edu-open-answer', attrs={'id': 'OA1'}):
            answers.append('Необходимо загрузить файл')

        return {
            'question': self.get_task_question(soup),
            'full_q': self.get_full_question(soup),
            'answer': answers
        }