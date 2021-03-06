from fabric import task
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'blog_zty'
    project_root_path = '~/apps/blog_zty/zblog'
    virtualenv_activate_path ='~/apps/blog_zty/bin'

    # 先杀掉screen进程
    with c.cd('~'):
        pass

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    #开启虚拟环境
    with c.cd(virtualenv_activate_path):
        c.run ('source activate')

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        c.run('pip install -r requirements.txt')
        c.run('python3 manage.py migrate')
        c.run('python3 manage.py collectstatic')

    # 重新启动screen
    with c.cd(supervisor_conf_path):
        pass