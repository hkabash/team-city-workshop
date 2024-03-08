import time
import pytest
import allure
from data.build_run_data import BuildRunResponseModel, BuildQueueResponse


class TestBuildRun:
    @allure.feature('Управление запусками билд конфигураций')
    @allure.story('Запуск билда')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка запуска билда')
    @allure.description('Тест проверяет запуск билда и его статус билд конфигурации после запуска')
    def test_build_run(self, super_admin, build_run_data):
        build_config_id = build_run_data.buildType.id
        expected_state = "queued"
        expected_build_queue_count = 0
        with allure.step('Отправка запроса на запуск билда'):
            response = super_admin.api_manager.build_run_api.run_build_config(build_run_data.model_dump()).text
            build_config_run_response = BuildRunResponseModel.model_validate_json(response)

        with allure.step('Проверка присутствия ожидаемой build_config_id в теле ответа на запрос о запуске билда'):
            with pytest.assume:
                assert build_config_run_response.buildTypeId == build_config_id, \
                    f"expected build config id is {build_config_id}, but '{build_config_run_response.buildTypeId}' given"

        with allure.step(f'Проверка присутствия ожидаемого статуса билда "{expected_state}" в теле ответа'
                         f' на запрос о запуске билда'):
            with pytest.assume:
                assert build_config_run_response.state == expected_state, \
                    f"expected build config run state is {expected_state}, but '{build_config_run_response.state}' given"

        time.sleep(2)  # дожидаемся, что билд собрался. В дальнейшем должно быть заменено на поллинг (создать декоратор)
        with allure.step("Отправка запроса на получение информации о статусе билда"):
            response = super_admin.api_manager.build_run_api.get_build_status(build_config_id).text
            build_queue_response = BuildQueueResponse.model_validate_json(response)

        with allure.step(f'Проверка количества непрошедших билдов"'):
            with pytest.assume:
                assert build_queue_response.count == expected_build_queue_count, \
                    f"expected builds run count is {expected_build_queue_count}, but '{build_queue_response.count}' given"
