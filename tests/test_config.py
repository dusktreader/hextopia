import pytest

from hextopia.config import HexConfig
from hextopia.exceptions import HexError


class TestCemConfig:

    def test_load_cem_config(self, find_data_file):
        """
        Verifies that a config can be loaded from file
        """
        test_file_path = find_data_file('test_normal_config.pydon')
        config = HexConfig.load_config(test_file_path)

        assert config.DEBUG
        assert not config.TESTING
        assert config.DATABASE_NAME == 'some_database_server'
        assert config.LOGGER_EMAIL_SUBJECT == 'why logging is the best'

        # Assert that defaults are also loaded
        assert config.DATABASE_SERVER == "localhost"

    def test__finalize_profiler(self, tmpdir):
        with pytest.raises(HexError) as err_info:
            HexConfig(PROFILE=True, PROFILE_DIR='/no/permission')._finalize_profiler()
        assert "PROFILE_DIR invalid or nonextant" in err_info.value.message

        with pytest.raises(HexError) as err_info:
            HexConfig(PROFILE=True, PROFILE_DIR='\0not a path\0')._finalize_profiler()
        assert "PROFILE_DIR invalid or nonextant" in err_info.value.message

        HexConfig(PROFILE=True, PROFILE_DIR=str(tmpdir))._finalize_profiler()
