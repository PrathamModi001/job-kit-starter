import subprocess
import json
import os
import time

class PlaywrightClient:
    def __init__(self, token='nITmoYPHpqf6ZZhs_DWZz_tJiCi-RaT70hNc2H-FfMg'):
        self.env = os.environ.copy()
        self.env['PLAYWRIGHT_MCP_EXTENSION_TOKEN'] = token
        self.proc = subprocess.Popen(
            ['npx', '-y', '@playwright/mcp@latest', '--extension'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env
        )
        self.req_id = 1
        self._init_session()

    def _rpc(self, method, params=None):
        expected_id = self.req_id
        msg = {'jsonrpc': '2.0', 'id': expected_id, 'method': method}
        if params is not None:
            msg['params'] = params
        self.req_id += 1
        self.proc.stdin.write(json.dumps(msg) + '\n')
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                return {}
            try:
                data = json.loads(line)
                if data.get('id') == expected_id:
                    return data
            except Exception:
                continue

    def _init_session(self):
        self._rpc('initialize', {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'job-automation', 'version': '1.0'}
        })
        self._rpc('notifications/initialized')

    def call_tool(self, name, arguments):
        res = self._rpc('tools/call', {'name': name, 'arguments': arguments})
        if 'error' in res:
            return {'error': res['error']}
        result = res.get('result', {})
        content = result.get('content', [])
        text_out = ''
        for item in content:
            if item.get('type') == 'text':
                text_out += item.get('text', '') + '\n'
        return {
            'isError': result.get('isError', False),
            'text': text_out,
            'raw': result
        }

    def navigate(self, url):
        res = self.evaluate(f"() => {{ window.location.href = '{url}'; }}")
        time.sleep(3)
        return res

    def snapshot(self):
        return self.call_tool('browser_snapshot', {})

    def evaluate(self, js_fn):
        return self.call_tool('browser_evaluate', {'function': js_fn})

    def evaluate_json(self, js_fn):
        res = self.evaluate(js_fn)
        text = res.get('text', '')
        if '### Result' in text:
            # isolate result part
            part = text.split('### Result')[1].strip()
            if part.startswith('\n'):
                part = part[1:].strip()
            # remove ### Ran Playwright code if present
            if '### Ran Playwright' in part:
                part = part.split('### Ran Playwright')[0].strip()
            # If it's a JSON string literal like "...", unquote or loads
            try:
                val = json.loads(part)
                if isinstance(val, str):
                    try:
                        return json.loads(val)
                    except:
                        return val
                return val
            except Exception as e:
                pass
        return None

    def click(self, element=None, ref=None):
        args = {}
        if element:
            args['element'] = element
        if ref:
            args['target'] = ref
        return self.call_tool('browser_click', args)

    def fill_form(self, form_data):
        return self.call_tool('browser_fill_form', {'form': form_data})

    def tabs(self, action='list'):
        return self.call_tool('browser_tabs', {'action': action})

    def close(self):
        try:
            self.proc.kill()
        except:
            pass

if __name__ == '__main__':
    client = PlaywrightClient()
    print('Testing navigate to Wellfound...')
    nav = client.navigate('https://wellfound.com/jobs')
    time.sleep(3)
    print('Done. Output snippet:', nav['text'][:200])
    client.close()
