import re

from docutils import nodes

# The obfuscation code was taken from
#
#   http://pypi.python.org/pypi/bud.nospam
#
# and was was released by Kevin Teague <kevin at bud ca> under
# a BSD license.


rot_13_trans = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
)


def rot_13_encrypt(line):
    """Rotate 13 encryption."""
    line = line.translate(rot_13_trans)
    line = re.sub('(?=[\\"])', r"\\", line)
    line = re.sub("\n", r"\n", line)
    line = re.sub("@", r"\\100", line)
    line = re.sub("\.", r"\\056", line)
    line = re.sub("/", r"\\057", line)
    return line


def js_obfuscated_text(text):
    """ROT 13 encryption with embedded in Javascript code to decrypt
    in the browser.

    """
    return """<script type="text/javascript">document.write(
              "%s".replace(/[a-zA-Z]/g,
              function(c){
                return String.fromCharCode(
                (c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);}));
                </script>""" % rot_13_encrypt(
        text
    )


def js_obfuscated_mailto(email, displayname=None):
    """ROT 13 encryption within an Anchor tag w/ a mailto: attribute"""
    if not displayname:
        displayname = email
    return js_obfuscated_text("""<a href="mailto:%s">%s</a>""" % (email, displayname))


# -- end bud.nospam


def email_role(
    typ, rawtext, text, lineno, inliner, options={}, content=[]  # noqa B006
):
    """Role to obfuscate e-mail addresses.

    Handle addresses of the form
    "name@domain.org"
    "Name Surname <name@domain.org>"
    """
    pattern = r"^(?:(?P<name>.*?)\s*<)?(?P<email>\b[-.\w]+@[-.\w]+\.[a-z]{2,4}\b)>?$"
    match = re.search(pattern, text)
    if not match:
        return [], []
    data = match.groupdict()

    obfuscated = js_obfuscated_mailto(email=data["email"], displayname=data["name"])
    node = nodes.raw("", obfuscated, format="html")
    return [node], []


def setup(app):
    app.add_role("email", email_role)
