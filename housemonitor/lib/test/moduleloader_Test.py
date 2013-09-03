'''
Created on Sep 17, 2012

@author: Gary
'''
import unittest
from housemonitor.lib.moduleloader import ModuleLoader
import logging.config
from mock import Mock, patch
import os


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'lib' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_loadm( self ):
        lmod = ModuleLoader()
        data = {'current values': 'abc'}
        lmod.load( data )

    def test_file_name( self ):
        m = ModuleLoader()
        self.assertEqual( m.file_name(), 'housemonitor.lib.moduleloader' )

    def test_load_with_exception_in_imp_read_module( self ):
        lmod = ModuleLoader()
        with patch( 'os.walk' ) as os.walk:
            os.walk.return_value = ["abc"]
            with patch( 'imp.find_module' ) as find_module:
                find_module.side_effect = ImportError( "ImportError in read_module" )
                data = {'current values': 'abc'}
                lmod.load( data )
                find_module.assert_called_once_with( "c", ["steps"] )

    def test_load_with_exception_in_imp_load_module( self ):
        lmod = ModuleLoader()
        with patch( 'os.walk' ) as os.walk:
            os.walk.return_value = ["abc"]
            with patch( 'imp.find_module' ) as find_module:
                find_module.return_value = ['a', 'b', 'c']
                with patch( 'imp.load_module' ) as load_module:
                    load_module.side_effect = ImportError( "ImportError in load_module" )
                    with patch( 'housemonitor.lib.moduleloader.ModuleLoader.close_file' ) as close_file:
                        data = {'current values': 'abc'}
                        lmod.load( data )
                        load_module.assert_called_once_with( "c", "a", "b", "c" )
                        find_module.assert_called_once_with( 'c', ['steps'] )
                        close_file.assert_called_once()

    def test_load_with_exception_in_package_instantiate_me( self ):
        lmod = ModuleLoader()
        with patch( 'os.walk' ) as os.walk:
            os.walk.return_value = ["abc"]
            with patch( 'imp.find_module' ) as find_module:
                find_module.return_value = ['a', 'b', 'c']
                with patch( 'imp.load_module' ) as load_module:
                    with patch( 'housemonitor.lib.moduleloader.ModuleLoader.get_class_name' ) as get_class_name:
                        with patch( 'housemonitor.lib.moduleloader.ModuleLoader.close_file' ) as close_file:
                            get_class_name.side_effect = AttributeError( "" )
                            data = {'current values': 'abc'}
                            lmod.load( data )
                            load_module.assert_called_once_with( "c", "a", "b", "c" )
                            find_module.assert_called_once_with( 'c', ['steps'] )
                            close_file.assert_called_once()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
