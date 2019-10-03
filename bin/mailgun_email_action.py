import sys, requests, json, re

def eprint(text):
    print >> sys.stderr, text

def check_inputs(config):
    if 'url' in config:
        matched = re.match(r'https?:\/\/[^.]+\.[^.]+.*',config['url'])
        if not matched:
            eprint("ERROR Invalid URL")
            return False
    else:
        eprint("ERROR No URL specified")
        return False
    if not 'api_key' in config:
        eprint("ERROR No API key specified")
        return False
    if 'email_type' in config:
        if config['email_type']!="html" and config['email_type']!="text":
            eprint("ERROR Invalid email type")
            return False
    else:
        eprint("ERROR No email type specified")
        return False
    if not 'to' in config:
        eprint("ERROR No to email address specified")
        return False
    if not 'from' in config:
        eprint("ERROR No from email address specified")
        return False

    return True

if len(sys.argv) > 1 and sys.argv[1] == "--execute":
    alert = json.load(sys.stdin)
    if check_inputs(alert['configuration']):
        #load config
        config = alert['configuration']
        url = config['url']
        email_type = config['email_type']
        content = config['content']
        to = config['to'].split(",")
        #construct call
        auth=('api',config['api_key'])
        data = {}
        data['from'] = config['from']
        data['to'] = to
        data['subject'] = config['subject']
        if email_type == "text":
            data['text'] = content
        elif email_type == "html":
            data['html'] = content
            data['text'] = "Error: HTML support is needed to view this email."
        #doit
        r = requests.post(url,auth=auth,data=data,verify=False)
        if r.status_code == 200:
            eprint("INFO 200: Success sending email")
        else:
            eprint("ERROR "+str(r.status_code)+": "+r.text)

    else:
        eprint("ERROR Invalid configuration detected. Stopped.")
else:
    eprint("FATAL No execute flag given")
