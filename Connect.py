from dataclasses import dataclass
from winrm.protocol import Protocol
from base64 import b64encode

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
        # self.session = winrm.Session(self.host, auth=(self.user, self.password))

    def test(self):
        # self.session.run_ps('dir')
        shell_id = self.session.open_shell()
        self.session.run_command(shell_id, 'echo 123')
        self.session.close_shell(shell_id)

    def get_cpu(self):
        ps_script = """$Server = $env:computername
            $cpu = Get-WMIObject –computername $Server win32_Processor
            "{0:0.0}" -f $cpu.LoadPercentage"""
        shell_id = self.session.open_shell()
        encoded_ps = b64encode(ps_script.encode('utf_16_le')).decode('ascii')
        command_id = self.session.run_command(shell_id, 'powershell -encodedcommand {0}'.format(encoded_ps))
        std_out, std_err, status_code = self.session.get_command_output(shell_id, command_id)
        self.session.close_shell(shell_id)
        result = str(std_out, encoding='utf-8')
        cpu_used = float(result.strip('\n').strip('\r'))
        print(cpu_used)
        return cpu_used

    def get_mem(self):
        script = """$mem = gwmi win32_OperatingSystem
            "{0:0.0}" -f ((($mem.TotalVisibleMemorySize-$mem.FreePhysicalMemory)/$mem.TotalVisibleMemorySize)*100)"""
        shell_id = self.session.open_shell()
        encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
        command_id = self.session.run_command(shell_id, 'powershell -encodedcommand {0}'.format(encoded_ps))
        std_out, std_err, status_code = self.session.get_command_output(shell_id, command_id)
        self.session.close_shell(shell_id)
        result = str(std_out, encoding='utf-8')
        mem_used = float(result.strip('\n').strip('\r'))
        print(mem_used)
        return mem_used
