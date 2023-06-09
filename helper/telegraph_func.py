from telegraph import Telegraph
import os

telegraph = Telegraph(os.getenv('telegraph'))
path = os.getenv('telegraph_path')

def get_page(return_content=True, return_html=True):
    page = telegraph.get_page(path=path,return_content=return_content,return_html=return_html)
    return page['title'], page['content']
    
def edit_page(title, html_content):
    page = telegraph.edit_page(path=path,title=title,html_content=html_content,author_name='bots')
    return
    
def logg(new_content):
    try:
        title, content = get_page()
        content = content + new_content
        edit_page(title, content)
        return True
    except:
        return False