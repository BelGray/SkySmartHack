import requests
import user_agent as u_ag

class SkySmartApi:

    base_url = "https://api-edu.skysmart.ru/api/v1/"
    default_task_url = ["https://edu.skysmart.ru/student/", "https://edu.skysmart.ru/student/task/"]

    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def headers(self):
        """Сгенерировать headers для HTTP-запроса"""
        user_agent = u_ag.generate_user_agent()
        return {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer ' + self.bearer_token,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
        }

    def get_tasks(self, taskHash):
        """Получить UUID всех заданий в тесте"""
        payload = "{\"taskHash\":\"" + taskHash + "\"}"
        headers = self.headers()
        get_tasks_request = requests.post(self.base_url + "task/preview", headers=headers, data=payload).json()
        return get_tasks_request['meta']['stepUuids']

    def get_meta(self, taskHash):
        """Получить мета-данные теста"""
        payload = "{\"taskHash\":\"" + taskHash + "\"}"
        headers = self.headers()
        get_meta_request = requests.post(self.base_url + "task/preview", headers=headers, data=payload).json()
        return get_meta_request["title"], get_meta_request["meta"]["path"]["module"]["title"]

    def get_task_content(self, task_uuid):
        """Получить контент задания по UUID в формате HTML"""
        headers = self.headers()
        get_task_content_request = requests.get(self.base_url + "content/step/load?stepUuid="+task_uuid, headers=headers).json()
        return get_task_content_request["content"]

    def cut_hash(self, message_content: str) -> tuple:
        """Получить уникальное значение теста из URL"""
        if message_content.startswith(self.default_task_url[1]):
            split_list = message_content.split("/")
            hash = split_list[5]
            return True, hash
        if message_content.startswith(self.default_task_url[0]):
            split_list = message_content.split("/")
            hash = split_list[4]
            return True, hash
        else:
            return False, None


