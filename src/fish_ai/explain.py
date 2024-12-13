# -*- coding: utf-8 -*-

from fish_ai import engine
import textwrap


def get_instructions(commandline):
    return [
        {
            'role': 'system',
            'content': textwrap.dedent('''\
            Respond with a maximum of three sentences which explain the fish
            shell command given by the user.

            The response must begin with a verb. The sentences should be
            written in {language}.

            In Cantonese, use "嘅" instead of "的", and use "係" instead of "是".

            You may use the following manpage to help explain the command:

            {manpage}''').format(
                language=engine.get_config('language') or 'English',
                manpage=engine.get_manpage(commandline.split()[0]))
        },
        {
            'role': 'user',
            'content': 'df -h'
        },
        {
            'role': 'assistant',
            'content': '列出系統上嘅所有磁碟'
        },
        {
            'role': 'user',
            'content': 'docker pull alpine:3'
        },
        {
            'role': 'assistant',
            'content': '從 DockerHub 拉取 Alpine 3 容器'
        },
        {
            'role': 'user',
            'content': 'sed -i "s/foo/bar/g" docker-compose.yml'
        },
        {
            'role': 'assistant',
            'content': '將文件 "docker-compose.yml" 中嘅所有 "foo" 字串替換為 "bar" 字串。'
        },
        {
            'role': 'user',
            'content': commandline
        }
    ]


def get_messages(commandline):
    return [engine.get_system_prompt()] + get_instructions(commandline)


def explain():
    engine.get_logger().info('----- BEGIN SESSION -----')

    commandline = engine.get_args()[0]

    try:
        engine.get_logger().debug('Explaining commandline: ' + commandline)
        response = engine.get_response(messages=get_messages(commandline))
        print('# ' + response.replace('\n', ' '), end='')
    except Exception as e:
        engine.get_logger().exception(e)
        # Leave the commandline untouched
        print(commandline, end='')

    engine.get_logger().info('----- END SESSION -----')
