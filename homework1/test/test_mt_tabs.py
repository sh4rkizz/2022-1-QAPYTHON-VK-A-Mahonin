import pytest

from base import BaseCase


class TestExample(BaseCase):
    @pytest.mark.UI
    def test_login(self, login):
        assert '/dashboard' in self.driver.current_url

    @pytest.mark.UI
    def test_profile_edit(self, login):
        answer = self.profile_edit()
        assert 'Контактная информация' in self.driver.title
        assert 'Информация успешно сохранена' in answer \
               or 'Максимально допустимое количество адресов электронной почты — 5' in answer

    @pytest.mark.UI
    @pytest.mark.parametrize(
        'button, expected_url',
        [
            pytest.param(
                'Аудитории',
                [
                        'https://target.my.com/segments/segments_list',
                        'https://target.my.com/segments'
                ]
            ),
            pytest.param(
                'Профиль',
                [
                        'https://target.my.com/profile/contacts',
                        'https://target.my.com/profile'
                ]
            )
        ]
    )
    def test_user_migrations(self, login, button: str, expected_url: list):
        self.user_migrations(button)
        assert self.driver.current_url in expected_url

    @pytest.mark.UI
    def test_logout(self, login):
        self.user_logout()
        assert 'Рекламная платформа myTarget — Сервис таргетированной рекламы' in self.driver.title
        assert 'https://target.my.com/' == self.driver.current_url
