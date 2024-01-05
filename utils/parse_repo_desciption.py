'''
    The language right here should de something like

    !!parse:
    falg1=param1,param2,param3|falg1=param1,param2,param3|
    falg3|flag4|
    :parse!!

    the flags are:
    show : 0 params permited
    dont_show: 0 params
    categories: n params 
    priority: 1 params should be a number
'''
def parse_repo_description(description : str, add_if_not_found : bool):
    categories = []
    priority = float('inf')
    include = add_if_not_found
    if description is None:
        description = ''
            
    begin = description.find("!!parse:")

    if description == '' or begin == -1:        
        return description, include, categories, priority 
    
    end = description.find(":parse!!")
    if end == -1:
        end = len(description)

    flags = []
    if begin != -1:
        flags = description[begin + 8: end].strip().split('|')
        flags = [x.split('=') for x in flags]

    if end == len(description):
        end -= 8

    if begin != -1:
        description = description[:begin].rstrip() + " " + description[end + 8:].lstrip()

    def show_f(pos):
        nonlocal include
        include = True
    def dont_show_f(pos):
        nonlocal include
        include = False
    def categories_f(pos):
        nonlocal  categories
        categories += [x.strip() for x in flags[pos][1].split(',')]
    def priority_f(pos):
        nonlocal priority
        priority = float(flags[pos][1].replace(',', '.'))

    PARSE_FUNCTIONS = {
        "show" : show_f, 
        "dont_show" : dont_show_f, 
        "categories" : categories_f,
        "priority" : priority_f 
    }

    for pos, flag in enumerate(flags):
        PARSE_FUNCTIONS[flag[0].strip()](pos)

    return description, include, categories, priority 
 
