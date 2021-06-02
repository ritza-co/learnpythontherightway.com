import os

cwd = os.getcwd()

# where the markdown files are
PATH_TO_MANU_REPO = os.path.normpath(os.path.join(cwd, "../../learn-python-the-right-way-book/manuscript/"))

# where we'll dump the HTML
PATH_TO_HTML_REPO = os.path.normpath(os.path.join(cwd, "../../learnpythontherightway.com/chapter"))

def get_title_metadesc(fp):
    with open(fp) as f:
        s = f.read().split("\n")[0]
        
        s = s.replace("# ", "")
        try:
            t, d = s.split(": ")
            title = f"{t} | Learn Python the Right Way"
            description = f"Learn about {d} in {t} of Learn Python the Right Way"
        except:
            title = f"{s} | Learn Python the Right Way"
            description = f"The {s} of Learn Python the Right Way"
    return title, description

def create_html(fp, title, description):
    out_fn = fp.split("/")[-1].replace(".md", ".html")
    print(out_fn)
    cmd = f'''pandoc "{fp}" --no-highlight -f markdown-auto_identifiers-citations -t html --lua-filter assets/fix-pre-code.lua -o out-temp.html'''
    print(cmd)
    os.system(cmd)
    
    with open("assets/template_pre.html") as f:
        pre = f.read()
        pre = pre.replace("{{title}}", title)
        pre = pre.replace("{{description}}", description)
    
    with open("assets/template_post.html") as f:
        post = f.read()
        
    with open("out-temp.html") as f:
        body = f.read()
        
    out_fp = os.path.join(PATH_TO_HTML_REPO, out_fn)
    with open(out_fp, "w") as f:
        f.write(pre + body + post)
        
def build_all():
    markdowns = os.listdir(PATH_TO_MANU_REPO)
    markdowns = [x for x in markdowns if x.endswith(".md")]
    for md in markdowns:
        fp = os.path.join(PATH_TO_MANU_REPO, md)
        print(fp)
        t, d = get_title_metadesc(fp)
        create_html(fp, t, d)
        
    # copy all images from book
    os.system("cp -r ../../learn-python-the-right-way-book/manuscript/resources/* ../chapter")
        
build_all()
