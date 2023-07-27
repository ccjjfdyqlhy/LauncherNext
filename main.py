
# EDIT ON 07/27/23
# To use the Launcher, visit [ip here]/launcher or by clicking the link in the main page.

import os
import subprocess
import zipfile
from nicegui import ui

cwd = os.getcwd()
os.system('mkdir lnxt')

def unpack(targetfile, targetdir):
    with zipfile.ZipFile(targetfile) as zf:
        try:
            zf.extractall(targetdir)
            print('[WARN] Unpack Successfully.')
        except Exception as e:
            print(f'[ERROR] Failed when unpacking: {e}')

def change_version():
    print('Version changed')

try:
    with open(os.path.join(cwd, 'version.lnxt')) as verreadf:
        verread = verreadf.read()
        versions = verread.split('\n')
        print('[INFO] Config loaded.')
except FileNotFoundError:
    print('[WARN] Config file not detected.')

@ui.page('/')
def index():
    ui.label('Demo').style('color: #6E93D6; font-size: 200%; font-weight: 300')

    def show(event):
        name = type(event.sender).__name__
        ui.notify('value已设定为:114514')

    ui.button('按钮 (连点来测手速)', on_click=lambda: ui.notify('点，点，点击'))

    with ui.row():
        ui.checkbox('向互联网泄露你的隐私', value=True)
        ui.switch('千万不要反复扳动这个开关!', on_change=show)

    ui.radio(['A', 'B', 'C'], value='A').props('inline')

    with ui.row():
        ui.input('输入文字...')
        ui.select(['One', 'Two'], value='One')

    ui.link('在浏览器中像专业人士一样启动Minecraft?!', '/launcher').classes('mt-8')

    class Demo:
        def __init__(self):
            self.number = 1

    demo = Demo()

    ui.upload(on_upload=lambda e: ui.notify(f'已上传 {e.name}')).classes('max-w-full')

    ui.textarea(label='大输入框子!', placeholder='你好啊\n你想在这里说些什么呢?\n赶紧敲进来吧~', on_change=lambda e: result.set_text('啊，你输入了: ' + e.value))
    result = ui.label()

    v = ui.checkbox('启用某个非常秘密的控制面板', value=False)
    with ui.column().bind_visibility_from(v, 'value'):
        knob = ui.knob(0.3, show_value=True)
        with ui.knob(color='orange', track_color='grey-2').bind_value(knob, 'value'):
            ui.icon('volume_up')
        ui.slider(min=1, max=3).bind_value(demo, 'number')
        ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
        ui.number().bind_value(demo, 'number')
        label = ui.label('变色龙?')
        ui.color_input(label='色', value='#000000', on_change=lambda e: label.style(f'color:{e.value}'))
        ui.date(value='2023-1-1', on_change=lambda e: result.set_text(e.value))
        result = ui.label()
        ui.time(value='11:45', on_change=lambda e: result.set_text(e.value))
        result = ui.label()

@ui.page('/launcher')
def launch():
    def login():
        print('[INFO] Launching login process')
        unpack('launcher.dll', os.path.join(cwd, 'lnxt', 'launcher'))
        os.system(os.path.join(cwd, 'lnxt', 'launcher', 'cmcl.exe account --login=authlib --address=https://littleskin.cn/api/yggdrasil'))
        os.system(f'del /q "{os.path.join(cwd, "lnxt", "launcher", "cmcl.exe")}"')

    def login_offline():
        username = 'Steve'
        print('[INFO] Launching login process')
        unpack('launcher.dll', os.path.join(cwd, 'lnxt', 'launcher'))
        os.system(os.path.join(cwd, 'lnxt', 'launcher', f'cmcl.exe account --login=offline --name={username}'))
        os.system(f'del /q "{os.path.join(cwd, "lnxt", "launcher", "cmcl.exe")}"')

    def register():
        print('[INFO] Launching browser')
        os.system('start https://littleskin.cn/')

    def check_update():
        print('[INFO] Checking update from the server...')

    def launch_mc(version):
        footer.toggle()
        launch_bt.visible = False
        ver_name = f'"{version}"'

        #[[Inject the launch code here]]

        launch_bt.visible = True

    with ui.header().classes(replace='row items-center') as header:
        ui.button(icon='style').props('flat color=white')
        with ui.tabs() as tabs:
            ui.tab('启动')
            ui.tab('版本')
            ui.tab('下载')
            ui.tab('Mod管理')
            ui.tab('选项')

    with ui.footer(value=False) as footer:
        with ui.column():
            ui.label('正在启动Minecraft').style('color: #FFFFFF; font-size: 200%; font-weight: 300')
            # To use the progressbar(which is developing) with no actural use:
            # progressbar = ui.linear_progress(value=0).props('instant-feedback')
            ui.label('请耐心等待...')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        launch_bt = ui.button(on_click=launch_mc, icon='rocket').props('fab')

    with ui.tab_panels(tabs, value='启动').classes('w-full'):
        with ui.tab_panel('启动'):
            ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.separator()
            with ui.column():
                ver_select = ui.select(versions, value=str(versions[0]))
                ui.button('管理登录', on_click=login).tooltip('管理Littleskin登录通行证')
                checkbox = ui.checkbox('使用离线登录 (你将无法使用多人游戏功能)')
                chk_var = ui.checkbox('补全文件 (会拖慢启动速度，但能解决大部分问题)')

        with ui.tab_panel('下载'):
            ui.label('Content of B')

        with ui.tab_panel('选项'):
            dark = ui.dark_mode()
            ui.label('个性化').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.label('切换主题:')
            ui.button('暗色', on_click=dark.enable)
            ui.button('亮色', on_click=dark.disable)
            ui.label('切换色调:')
            ui.button('默认蓝', on_click=lambda: ui.colors())
            ui.button('低调灰', on_click=lambda: ui.colors(primary='#555'))
            ui.separator()
            ui.label('Minecraft实例').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            with ui.column():
                switch1 = ui.switch('启用版本隔离')
                switch2 = ui.switch('强制使用指定Java')
                switch3 = ui.switch('DUMMY SWITCH')
                switch4 = ui.switch('switch me')
                switch5 = ui.switch('switch me')
                switch6 = ui.switch('switch me')
            ui.label('启动选项').style('color: #6E93D6; font-size: 200%; font-weight: 300')
ui.run(title='webUI')
