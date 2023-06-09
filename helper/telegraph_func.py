from telegraph import Telegraph
import os

telegraph = Telegraph(os.getenv('telegraph'))
path = os.getenv('telegraph_path')
    
def logg(new_content):
    page = telegraph.get_page(path=path,return_content=True,return_html=True)
    title, content = page['title'], page['content']
    content = new_content + content
    telegraph.edit_page(path=path,title=title,html_content=content,author_name='bots')
    return