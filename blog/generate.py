import os
import subprocess
import string

ITEM_TEMPLATE = './template.html'
INDEX_TEMPLATE = './index-template.html'
SLUG_FORMAT = "{}\n{}\n{}\n<a href='{}'>Read more...</a>"

def blog_files():
    allfiles = sorted(os.listdir('.'))
    allfiles.reverse()
    for x in allfiles:
        if x.endswith('text'):
            yield x

def generate_html(textFile):
    text = open(textFile, 'r')    
    sp = subprocess.Popen("./Markdown.pl", stdin=text, stdout=subprocess.PIPE)
    html = sp.communicate()
    text.close()
    return html[0]

def save_html_in_template(htmlFile, markdown, template):
    title = markdown.splitlines()[0].replace('<h1>', '').replace('</h1>', '')
    complete = template.substitute(filename=htmlFile, blogitem=markdown, title=title)
    output = open(htmlFile, 'w')  
    output.write(complete)
    output.close()
    

def read_template(filename):
    templateFile = open(filename, 'r')
    templateData = templateFile.read()
    templateFile.close()
    return string.Template(templateData)

def main():
    item_template = read_template(ITEM_TEMPLATE)
    slugs = []
    new_generated = False
    
    for textFile in blog_files():
        print 'Processing {}...'.format(textFile)
        htmlFile = textFile.replace('.text', '.html')
        markdown = generate_html(textFile)        
        if not os.access(htmlFile, os.F_OK):
            save_html_in_template(htmlFile, markdown, item_template)
            new_generated = True
        else:
            print ' {} already exists; skipping generation.'.format(htmlFile)
        
        lines = markdown.splitlines()
        header = lines[0].replace('<h1>', "<h1><a href='{}'>".format(htmlFile))
        header = header.replace('</h1>', '</a></h1>')
        slugs.append(SLUG_FORMAT.format(header,lines[2],lines[4], htmlFile))
    
    if not new_generated:
        print 'No new files generated - bailing out.'
        return
    
    index_template = read_template(INDEX_TEMPLATE)
    indexFile = open('./index.html', 'w')
    indexFile.write(index_template.substitute(blogindex="\n<hr/>\n".join(slugs)))
    indexFile.close()
    print 'Wrote index; complete.'
    

if __name__ == '__main__':
    main()