import pytest

from mysql.scripts import LogBuilder
from mysql.models import AllRequests, \
    RequestsByType, \
    TheMostFrequentRequests, \
    ClientBasedErrors, \
    ServerBasedErrors


class BaseMySQL:
    mysql = logbuilder = None

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.logbuilder = LogBuilder(client=mysql_client)


@pytest.mark.mysql
class TestMySQL(BaseMySQL):
    def test_count_requests(self):
        self.logbuilder.count_requests()
        table_content = (
            self.mysql
                .session
                .query(AllRequests)
                .all()
        )

        assert len(table_content) == 1

    def test_count_requests_by_type(self):
        line_counter = self.logbuilder.count_requests_by_type()
        table_content = (
            self.mysql
                .session
                .query(RequestsByType)
                .all()
        )

        assert len(table_content) == line_counter

    def test_most_frequent_requests(self):
        line_counter = self.logbuilder.count_most_frequent_requests()
        table_content = (
            self.mysql
                .session
                .query(TheMostFrequentRequests)
                .all()
        )

        assert len(table_content) == line_counter

    def test_biggest_client_based_errors(self):
        line_counter = self.logbuilder.count_biggest_client_based_errors()
        table_content = (
            self.mysql
                .session
                .query(ClientBasedErrors)
                .all()
        )

        assert len(table_content) == line_counter

    def test_count_requests_with_server_error(self):
        line_counter = self.logbuilder.count_requests_with_server_error()
        table_content = (
            self.mysql
                .session
                .query(ServerBasedErrors)
                .all()
        )

        assert len(table_content) == line_counter
