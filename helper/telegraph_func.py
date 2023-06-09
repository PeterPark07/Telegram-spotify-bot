from telegraph import Telegraph
import os

telegraph = Telegraph(os.getenv('telegraph'))
path = os.getenv('telegraph_path')

def get_page(path, return_content=True, return_html=True):
    page = telegraph.get_page(
        path=path,
        return_content=return_content,
        return_html=return_html
    )
    return page['title'], page['content']
    
title, content = get_page(path)
    
def edit_page(path, title, html_content=None, author_name=None, author_url=None, return_content=False):
    page = telegraph.edit_page(
        path=path,
        title=title,
        html_content=html_content,
        author_name=author_name,
        author_url=author_url,
        return_content=return_content
    )
    return
    
def logg(new_content):
    try:
        title, content = get_page(path)
        content = content + new_content
        edit_page(path, title, content, 'bots')
        return True
    except:
        return False