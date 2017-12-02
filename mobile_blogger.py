import appex
import console
import keychain
import dialogs
import gitlab
import re
import dropbox
import config as cfg

from string import Template
from datetime import date
from time import strftime
from dropbox.exceptions import AuthError


def slug(text):
    permitted_chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789-'

    for char in text:
        if char not in permitted_chars:
            text = text.replace(char, '-')

    while '--' in text:
        text = text.replace('--', '-')

    return ''.join(text)


def extract_title(text):
    lines = re.split('\n+', text, 2)
    title = re.sub('^#+\s+', '', lines[0])

    if len(lines) < 2:
        return title, None

    index = 1
    if re.search('^(=|-)+$', lines[1]):
        index = 2

    return title, '\n'.join(lines[index:])


def process_string_array(array):
    array = array.strip()
    output = []
    for item in array.split():
        output.append(item)
    output = ','.join(output)
    output = '[' + output + ']'
    return output


class MobileBlogger:
    def __init__(self, gitlab_url, gitlab_repo, gitlab_token, dbx_token):
        self.gitlab_url = gitlab_url
        self.gitlab_repo = gitlab_repo
        self.gitlab_token = gitlab_token
        self.dbx_token = dbx_token
        self._latest_commit = None
        self._initialize_clients()

    def _initialize_clients(self):
        self._gl = gitlab.Gitlab(
            self.gitlab_url,
            self.gitlab_token,
            api_version=4
        )
        self._gl.auth()
        self._dbx = dropbox.Dropbox(self.dbx_token)

    def _get_latest_commit(self, reload=False):
        if self._latest_commit is None or reload:
            self.project = self._gl.projects.get(self.gitlab_repo)
            commits = self.project.commits.list()
            self._latest_commit = commits[0]

        return self._latest_commit

    def _prepend_metadata(self, text, metas):
        metas['comments'] = str(metas['comments']).lower()
        template = '''---
layout:     ${layout}
title:      "${title}"
author:     "${author}"
'''
        draft = metas['draft']
        if draft:
            metas['draft'] = str(draft).lower()
            template += '''draft:      ${draft}
'''

        template += '''categories: ${categories}
date:       ${date}
tags:       ${tags}
comments:   ${comments}
excerpt:    "${excerpt}"
'''

        fip = metas['feature_img_path']
        if fip and fip.strip():
            template += '''image:
    feature: ${feature_img_path}
'''
            fim = metas['feature_img_wide']
            if fim and fim.strip():
                metas['feature_img_wide'] = str(fim).lower()
                template += '''    wide:    ${feature_img_wide}
'''
            fic = metas['feature_img_caption']
            if fic and fic.strip():
                template += '''    caption: ${feature_img_caption}
'''

        template += '''---

'''
        return Template(template).substitute(metas) + text

    def create_new_post(self, title, text, metas):
        default_metas = {
            'layout': 'post',
            'date': strftime("%Y-%m-%d"),  # %H:%M:%S"),
            'title': title
        }

        default_metas.update(metas)
        branch = default_metas['branch']
        filename = default_metas['filename']
        del default_metas['branch']
        del default_metas['filename']

        text = self._prepend_metadata(text, default_metas)
        latest_commit = self._get_latest_commit()

        print(text)
        sys.exit(0)

        filepath_prefix = cfg.dropbox['drafts_dir_prefix'] if metas['draft'] else cfg.dropbox['posts_dir_prefix']

        commit_data = {
            'branch': 'master',
            'commit_message': 'new post: ' + title,
            'actions': [
                {
                    'action': 'create',
                    'file_path': filepath_prefix + filename,
                    'content': text
                }
            ]
        }
        commit = self.project.commits.create(commit_data)
        return text

    def sync_to_dropbox(self, filename, draft, text):
        file_root = cfg.dropbox['directory_root']
        dir_prefix = cfg.dropbox['drafts_dir_prefix'] if draft else cfg.dropbox['posts_dir_prefix']
        full_path = file_root + dir_prefix + filename
        output = str.encode(text)
        try:
            self._dbx.files_upload(output, full_path)
        except AuthError as err:
            print(err)


def main():
    if not appex.is_running_extension():
        print('running in pythonista--using test data\n')
        text = '''## Test Data
Generic test data!'''
    else:
        text = appex.get_text()

    if text:
        author = cfg.post['post_author']
        gitlab_url = cfg.post['gitlab_url']
        gitlab_user = cfg.post['gitlab_user']
        gitlab_repo = cfg.post['gitlab_repo']
        gitlab_token = keychain.get_password('gitlab_token', gitlab_user) or ''
        dbx_token = keychain.get_password('dbx_token', gitlab_user) or ''

        (title, text) = extract_title(text)
        filename = '%s-%s.md' % (date.today(), slug(title))

        dbx_fields = (
            'Dropbox Settings',
            [
                dict(title='Dropbox Token', key='dbx_token', type='text', value=dbx_token, autocorrection=False,
                     autocapitalization=False)
            ]
        )

        gitlab_fields = (
            'Gitlab Settings',
            [
                dict(title='Gitlab URL', key='gitlab_url', type='text', value=gitlab_url, autocorrection=False,
                     autocapitalization=False),
                dict(title='Gitlab User', key='gitlab_user', type='text', value=gitlab_user, autocorrection=False,
                     autocapitalization=False),
                dict(title='Gitlab Token', key='gitlab_token', type='text', value=gitlab_token, autocorrection=False,
                     autocapitalization=False),
                dict(title='Repo', key='gitlab_repo', type='text', value=gitlab_repo, autocorrection=False,
                     autocapitalization=False)
            ]
        )

        posting_fields = (
            'Post Settings',
            [
                dict(title='Title', key='title', type='text', value=title),
                dict(title='Author', key='author', type='text', value=author),
                dict(title='Draft', key='draft', type='switch', value=True),
                dict(title='Layout', key='layout', type='text', value='post', autocorrection=False,
                     autocapitalization=False),
                dict(title='Tags', key='tags', type='text', value=''),
                dict(title='Categories', key='categories', type='text', value=''),
                dict(title='Comments', key='comments', type='switch', value=True),
                dict(title='Excerpt', key='excerpt', type='text', value=''),
                dict(title='ImagePath', key='feature_img_path', type='text', value=''),
                dict(title='ImageWide', key='feature_img_wide', type='switch', value=False),
                dict(title='ImageCaption', key='feature_img_caption', type='text', value=''),
                dict(title='Filename', key='filename', type='text', value=filename, autocorrection=False,
                     autocapitalization=False)
            ],
            'Separate tags/categories with spaces'
        )

        results = dialogs.form_dialog(title='publish new post', sections=[
            posting_fields,
            gitlab_fields,
            dbx_fields
        ])

        if results is None:
            console.hud_alert('posting was cancelled', 'error')
            return

        results['tags'] = process_string_array(results['tags'])
        results['categories'] = process_string_array(results['categories'])

        metas = {
            'layout': results['layout'],
            'author': results['author'],
            'draft': results['draft'],
            'tags': results['tags'],
            'categories': results['categories'],
            'comments': results['comments'],
            'excerpt': results['excerpt'],
            'feature_img_path': results['feature_img_path'],
            'feature_img_wide': results['feature_img_wide'],
            'feature_img_caption': results['feature_img_caption'],
            'branch': 'master',
            'filename': results['filename']
        }

        if gitlab_token != results['gitlab_token']:
            keychain.set_password('gitlab_token', results['gitlab_user'], results['gitlab_token'])

        if dbx_token != results['dbx_token']:
            keychain.set_password('dbx_token', results['gitlab_user'], results['dbx_token'])

        console.show_activity()
        mb = MobileBlogger(results['gitlab_url'], results['gitlab_repo'], results['gitlab_token'], results['dbx_token'])
        file = mb.create_new_post(results['title'], text, metas)
        mb.sync_to_dropbox(results['filename'], results['draft'], file)
        console.hud_alert('new post created!')
    else:
        print('no input text found')


if __name__ == '__main__':
    main()
