import sass
import os
import os.path as path
import shutil
import jsmin

# css compile
css_from_dir = 'private/assets/scss'
css_to_dir = 'app/static/assets/css'
if not path.isdir(css_from_dir):
    os.mkdir(css_from_dir)
if not path.isdir(css_to_dir):
    os.mkdir(css_to_dir)

# scss = """\
# $theme_color: #cc0000;
# body {
#     background-color: $theme_color;
# }
# """
# with open(css_from_dir + '/example.scss', 'w') as example_scss:
#     example_scss.write(scss)

print('SASS Compile: working...')
sass.compile(dirname=(css_from_dir, css_to_dir), output_style='compressed')
# with open(to_dir + '/example.css') as example_css:
#     print(example_css.read())
print('SASS Compile: successfully.')


# js compile
js_from_dir = 'private/assets/jss'
js_to_dir = 'app/static/assets/js'
if not path.isdir(js_from_dir):
    os.mkdir(js_from_dir)
if not path.isdir(js_to_dir):
    os.mkdir(js_to_dir)

print('JS Minify: working...')
for src_dir, dirs, files in os.walk(js_from_dir):
    from_src_dir = src_dir[len(js_from_dir) + 1:].strip()
    for onefile in files:
        oneftitle = onefile[:len(onefile) -
                            3] if onefile.endswith('.js') else onefile
        
        fpath = ('/' + from_src_dir if len(from_src_dir)
                 > 0 else '') + '/' + oneftitle

        src_filename = (js_from_dir + fpath + '.js')
        dst_filename = (js_to_dir + fpath + '.min.js')

        with open(src_filename) as src_js_file:
            minified = jsmin.jsmin(src_js_file.read())
            bdir = path.dirname(dst_filename)
            print('JS Write: ', dst_filename)
            if not path.isdir(bdir):
                os.mkdir(bdir)
            with open(dst_filename, 'w') as dst_js_file:
                dst_js_file.write(minified)
print('JS Minify: successfully.')