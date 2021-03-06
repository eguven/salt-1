# coding: utf-8

# Import Python libs
import os

# Import Salt Testing libs
import integration

# Import Salt libs
import salt.wheel


class WheelModuleTest(integration.ClientCase):
    eauth_creds = {
        'username': 'saltdev_auto',
        'password': 'saltdev',
        'eauth': 'auto',
    }

    def setUp(self):
        '''
        Configure an eauth user to test with
        '''
        self.wheel = salt.wheel.Wheel(self.get_opts())

    def test_master_call(self):
        '''
        Test executing master_call with lowdata

        The choice of using key.list_all for this is arbitrary and should be
        changed to some mocked function that is more testing friendly.
        '''
        low = {
            'client': 'wheel',
            'fun': 'key.list_all',
        }
        low.update(self.eauth_creds)

        self.wheel.master_call(**low)

    def test_token(self):
        '''
        Test executing master_call with lowdata

        The choice of using key.list_all for this is arbitrary and should be
        changed to some mocked function that is more testing friendly.
        '''
        import salt.auth

        opts = self.get_opts()
        self.mkdir_p(os.path.join(opts['root_dir'], 'cache', 'tokens'))

        auth = salt.auth.LoadAuth(opts)
        token = auth.mk_token(self.eauth_creds)

        self.wheel.master_call(**{
            'client': 'wheel',
            'fun': 'key.list_all',
            'token': token['token'],
        })

    def test_cmd_sync(self):
        low = {
            'client': 'wheel',
            'fun': 'key.list_keys',
        }
        low.update(self.eauth_creds)

        self.wheel.cmd_sync(low)

    def test_cmd_async(self):
        low = {
            'client': 'wheel_async',
            'fun': 'key.list_keys',
        }
        low.update(self.eauth_creds)

        self.wheel.cmd_async(low)

    def test_cmd_sync_w_arg(self):
        low = {
            'fun': 'key.finger',
            'match': '*',
        }
        low.update(self.eauth_creds)

        ret = self.wheel.cmd_sync(low)
        self.assertIn('return', ret.get('data', {}))

    def test_wildcard_auth(self):
        low = {
            'username': 'the_s0und_of_t3ch',
            'password': 'willrockyou',
            'eauth': 'auto',
            'fun': 'key.list_all',
        }

        self.wheel.cmd_sync(low)

if __name__ == '__main__':
    from integration import run_tests
    run_tests(WheelModuleTest, needs_daemon=True)
