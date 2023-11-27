import os, json, ast, copy, importlib

import gradio as gr

data = [
    {
        '<|model|>' : 'importlib.import_module(\'modules.shared\').model_name'
    },
    {
        '<|now|>' : '__import__(\'datetime\').datetime.now().strftime(\'%Y%m%d-%H-%M-%S\')'
    },
    {
        'one bar prison' : '\"one bar prison (A device that is meant for keeping the recipient in place by having them stand on top of a bar with a dildo or buttplug at the end.)\"'
    }
]

# get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# check if the to_replace.json file exists, if not, create it
replace_file = os.path.join(current_dir, "to_replace.json")
if not os.path.isfile(replace_file):
    with open(replace_file, "w") as f:
        f.write(json.dumps(data))
        


def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)

        return result
def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"),globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"),globals())


def input_modifier(string, state):
    """
    This function is applied to the model inputs.
    """
    with open(replace_file) as user_file:
      file_contents = user_file.read()    
      
    mydata = json.loads(file_contents)
    
    for commands in mydata:
        print(commands)
        for attribute, value in commands.items():
            string = string.replace(attribute, exec_with_return(value))
    
    return string


