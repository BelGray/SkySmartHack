import task_answer
from skysmart_api import SkySmartApi
from secret import token
#в переменной token находится токен от вашего аккаунта в SkySmart

SSApi = SkySmartApi(token)
AnsBody = task_answer.TaskAnswerObject("nexemiduke")

# print(tid := SSApi.get_tasks("nexemiduke"))
# print(SSApi.get_task_content('58274ae8-b358-4059-9ebd-c175f165dde5'))
print(AnsBody.get_task_answer(SSApi.get_task_content('58274ae8-b358-4059-9ebd-c175f165dde5')))
