from dataclasses import dataclass
from winrm.protocol import Protocol

@dataclass
class link:

    host: str
    user: str
    password: str
    session: None

    def __post_init__(self):
        self.get_session()

    def get_session(self):
        self.session = Protocol(
            endpoint='http://' + self.host + ':5985/wsman',
            transport='ntlm',
            username='administrator',
            password='LRTabc123.',
            server_cert_validation='ignore')

    def test(self):
        shell_id = self.session.open_shell()
        command_id = self.session.run_command(shell_id, 'ipconfig', ['/all'])
        std_out, std_err, status_code = self.session.get_command_output(shell_id, command_id)
        self.session.cleanup_command(shell_id, command_id)
        print(std_out, status_code)
        self.session.close_shell(shell_id)